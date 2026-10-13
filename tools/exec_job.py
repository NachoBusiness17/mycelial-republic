"""L3 Job Object containment for the shell door (tools/code_execution.py).

Port-order lane P4 (2026-10-07, watch/inbox/port_wave_20261007/p4_shell_door.md).
pywin32 when the venv has it, ctypes otherwise. Gives: process memory cap,
kill-on-close (the whole tree dies with the handle even on hang or harness
crash), and UI restrictions (clipboard, global atoms, exit windows). Does NOT
give: filesystem, network or registry isolation; that is Windows-without-a-
container reality and is stated here so nobody reads the job as a sandbox.
"""
from __future__ import annotations

import ctypes
import os
import sys

_JOB_UI_RESTRICTIONS = 0x0004 | 0x0008 | 0x0040 | 0x0002  # READCLIP | WRITECLIP | GLOBALATOMS | EXITWINDOWS

_DEFAULT_MEM_CAP_MB = 512
_MIN_MEM_CAP_MB = 32


def mem_cap_bytes() -> int:
    """Per-call cap so a test or lane can tighten it; floor 32 MB so a
    fat-fingered env cannot disable the limit entirely."""
    mb = _DEFAULT_MEM_CAP_MB
    raw = os.environ.get("MAG_EXEC_MEM_CAP_MB")
    if raw is not None:
        try:
            mb = int(raw)
        except ValueError:
            mb = _DEFAULT_MEM_CAP_MB  # junk env falls back to the default cap
    return max(_MIN_MEM_CAP_MB, mb) * 1024 * 1024


class Job:
    """Minimal Job Object wrapper, factory-agnostic (pywin32 or ctypes)."""

    def __init__(self, mem_cap: int) -> None:
        self._win32 = None
        self._ct = None
        self._handle = None
        if sys.platform != "win32":
            raise OSError("job objects are win32-only")
        try:
            import win32job
        except ImportError:
            win32job = None  # venv without pywin32: the ctypes factory below
        if win32job is not None:
            self._win32 = win32job
            self._handle = win32job.CreateJobObject(None, "")
            info = win32job.QueryInformationJobObject(
                self._handle, win32job.JobObjectExtendedLimitInformation)
            info["BasicLimitInformation"]["LimitFlags"] |= (
                win32job.JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE
                | win32job.JOB_OBJECT_LIMIT_PROCESS_MEMORY)
            info["ProcessMemoryLimit"] = mem_cap
            win32job.SetInformationJobObject(
                self._handle, win32job.JobObjectExtendedLimitInformation, info)
            ui = win32job.QueryInformationJobObject(
                self._handle, win32job.JobObjectBasicUIRestrictions)
            win32job.SetInformationJobObject(
                self._handle, win32job.JobObjectBasicUIRestrictions,
                {"UIRestrictionsClass": ui.get("UIRestrictionsClass", 0) | _JOB_UI_RESTRICTIONS})
            return
        self._ct = ctypes.windll.kernel32  # type: ignore[attr-defined]
        kt = self._ct
        kt.CreateJobObjectW.restype = ctypes.c_void_p
        handle = kt.CreateJobObjectW(None, None)
        if not handle:
            raise OSError(f"CreateJobObjectW failed: {ctypes.GetLastError()}")
        self._handle = handle
        info = self._ctypes_ext_info()
        info.BasicLimitInformation.LimitFlags |= 0x2000 | 0x100  # KILL_ON_CLOSE | PROCESS_MEMORY
        info.ProcessMemoryLimit = mem_cap
        if not kt.SetInformationJobObject(
                ctypes.c_void_p(handle), 9, ctypes.byref(info), ctypes.sizeof(info)):
            kt.CloseHandle(ctypes.c_void_p(handle))
            raise OSError(f"SetInformationJobObject failed: {ctypes.GetLastError()}")
        if not kt.SetInformationJobObject(
                ctypes.c_void_p(handle), 4,  # 4 = JobObjectBasicUIRestrictions
                ctypes.byref(ctypes.c_ulong(_JOB_UI_RESTRICTIONS)),
                ctypes.sizeof(ctypes.c_ulong)):
            kt.CloseHandle(ctypes.c_void_p(handle))
            raise OSError(f"SetInformationJobObject(UI) failed: {ctypes.GetLastError()}")

    @staticmethod
    def _ctypes_ext_info():
        class IO_COUNTERS(ctypes.Structure):
            _fields_ = [(n, ctypes.c_ulonglong) for n in (
                "ReadOperationCount", "WriteOperationCount", "OtherOperationCount",
                "ReadTransferCount", "WriteTransferCount", "OtherTransferCount")]

        class BASIC_LIMIT_INFO(ctypes.Structure):
            _fields_ = [
                ("PerProcessUserTimeLimit", ctypes.c_longlong),
                ("PerJobUserTimeLimit", ctypes.c_longlong),
                ("LimitFlags", ctypes.c_ulong),
                ("MinimumWorkingSetSize", ctypes.c_size_t),
                ("MaximumWorkingSetSize", ctypes.c_size_t),
                ("ActiveProcessLimit", ctypes.c_ulong),
                ("Affinity", ctypes.c_size_t),
                ("PriorityClass", ctypes.c_ulong),
                ("SchedulingClass", ctypes.c_ulong),
            ]

        class EXT_LIMIT_INFO(ctypes.Structure):
            _fields_ = [
                ("BasicLimitInformation", BASIC_LIMIT_INFO),
                ("IoInfo", IO_COUNTERS),
                ("ProcessMemoryLimit", ctypes.c_size_t),
                ("JobMemoryLimit", ctypes.c_size_t),
                ("PeakProcessMemoryUsed", ctypes.c_size_t),
                ("PeakJobMemoryUsed", ctypes.c_size_t),
            ]
        return EXT_LIMIT_INFO()

    def assign(self, proc_handle: int) -> None:
        if self._win32:
            self._win32.AssignProcessToJobObject(self._handle, proc_handle)
            return
        if not self._ct.AssignProcessToJobObject(
                ctypes.c_void_p(self._handle), ctypes.c_void_p(proc_handle)):
            raise OSError(f"AssignProcessToJobObject failed: {ctypes.GetLastError()}")

    def terminate(self) -> None:
        """Kill every process in the job (timeout path; tree-wide)."""
        if self._win32:
            self._win32.TerminateJobObject(self._handle, 1)
            return
        self._ct.TerminateJobObject(ctypes.c_void_p(self._handle), 1)

    def close(self) -> None:
        """Close the handle: KILL_ON_JOB_CLOSE makes this a tree-wide backstop."""
        if self._handle is None:
            return
        if self._win32:
            self._handle.Close()
        else:
            self._ct.CloseHandle(ctypes.c_void_p(self._handle))
        self._handle = None
