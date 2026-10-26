// bash.exe forwarder shim (estate root), GALA wave5-repair fold-gate fix, 2026-09-29.
//
// Cause: the GALA wave5 workflow re-runs its fold gate as spawn("bash", [FOLD_SH, LANES, N]).
// On Windows, CreateProcess resolves bare "bash" as: parent exe dir -> parent cwd ->
// System32 -> PATH. System32\bash.exe is the WSL launcher; its default distro was
// docker-desktop (no /bin/bash) => execvpe(/bin/bash) failed, exit 1 (gate never ran).
// Even with a Linux default distro, WSL bash cannot open the gate's absolute C:/... script
// path (exit 127), while the gate script is written for Windows-side bash (it execs the
// repo venv's Windows python.exe).
//
// Fix: this shim sits in the estate root = the harness's working directory, so CreateProcess
// finds it BEFORE System32. It re-execs Git Bash with the identical argument line and
// inherited std handles, so every bare-bash spawn from this directory gets real Git Bash.
// It forwards verbatim: no arguments are added, dropped, or rewritten (except argv0).
//
// Rebuild: C:\Windows\Microsoft.NET\Framework64\v4.0.30319\csc.exe /nologo /out:bash.exe bash_shim_forwarder.cs
using System;
using System.Runtime.InteropServices;

class BashForwarder {
    [DllImport("kernel32.dll", SetLastError = true, CharSet = CharSet.Unicode)]
    static extern bool CreateProcess(string app, string cmd, IntPtr pa, IntPtr ta, bool inh,
        uint flags, IntPtr env, string cwd, ref STARTUPINFO si, out PROCESS_INFORMATION pi);
    [DllImport("kernel32.dll", SetLastError = true)]
    static extern IntPtr GetStdHandle(int which);
    [DllImport("kernel32.dll", SetLastError = true)]
    static extern uint WaitForSingleObject(IntPtr h, uint ms);
    [DllImport("kernel32.dll", SetLastError = true)]
    static extern bool GetExitCodeProcess(IntPtr h, out int code);
    [DllImport("kernel32.dll", SetLastError = true)]
    static extern bool CloseHandle(IntPtr h);

    const uint INFINITE = 0xFFFFFFFF;
    const int STD_INPUT_HANDLE = -10, STD_OUTPUT_HANDLE = -11, STD_ERROR_HANDLE = -12;
    const uint STARTF_USESTDHANDLES = 0x00000100;

    // Exact Win32 STARTUPINFOW field order; a wrong layout would corrupt the CreateProcess call.
    [StructLayout(LayoutKind.Sequential, CharSet = CharSet.Unicode)]
    struct STARTUPINFO {
        public uint cb;
        public string lpReserved;
        public string lpDesktop;
        public string lpTitle;
        public uint dwX, dwY, dwXSize, dwYSize, dwXCountChars, dwYCountChars, dwFillAttribute, dwFlags;
        public ushort wShowWindow, cbReserved2;
        public IntPtr lpReserved2;
        public IntPtr hStdInput, hStdOutput, hStdError;
    }
    [StructLayout(LayoutKind.Sequential)]
    struct PROCESS_INFORMATION {
        public IntPtr hProcess, hThread;
        public uint pid, tid;
    }

    const string TARGET = "C:\\Program Files\\Git\\bin\\bash.exe";

    static int Main() {
        string cl = Environment.CommandLine;
        // Strip argv0 (quoted or bare) from the raw command line, keep the rest verbatim.
        string rest;
        if (cl.Length > 0 && cl[0] == '"') {
            int q = cl.IndexOf('"', 1);
            rest = q < 0 ? "" : cl.Substring(q + 1);
        } else {
            int s = cl.IndexOf(' ');
            rest = s < 0 ? "" : cl.Substring(s);
        }
        string childCmd = "\"" + TARGET + "\"" + rest;

        STARTUPINFO si = new STARTUPINFO();
        si.cb = (uint)Marshal.SizeOf(typeof(STARTUPINFO));
        si.dwFlags = STARTF_USESTDHANDLES;
        si.hStdInput = GetStdHandle(STD_INPUT_HANDLE);
        si.hStdOutput = GetStdHandle(STD_OUTPUT_HANDLE);
        si.hStdError = GetStdHandle(STD_ERROR_HANDLE);

        PROCESS_INFORMATION pi;
        if (!CreateProcess(TARGET, childCmd, IntPtr.Zero, IntPtr.Zero, true, 0,
                IntPtr.Zero, null, ref si, out pi)) {
            int err = Marshal.GetLastWin32Error();
            Console.Error.WriteLine("bash.exe shim: cannot exec " + TARGET + " (Win32 error " + err + ")");
            return 127;
        }
        WaitForSingleObject(pi.hProcess, INFINITE);
        int code;
        GetExitCodeProcess(pi.hProcess, out code);
        CloseHandle(pi.hProcess);
        CloseHandle(pi.hThread);
        return code;
    }
}
