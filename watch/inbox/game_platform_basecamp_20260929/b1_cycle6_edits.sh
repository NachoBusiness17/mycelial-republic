#!/bin/bash
# B1 bots-port cycle-6 canonical edits, 2026-09-29.
# Two late-surfacing Boost 1.90 remnants in the game lib (first time the build
# got past the Bots module): Metric.h/.cpp io_context::work (ledger fix-5 gap -
# only NetworkThread.hpp had been converted) and WorldSession.cpp to_ulong.
# CRLF law: no $-anchored patterns. No '&' in sed replacement text.
set -e
C=/mnt/c/Users/foste/Documents/projects/local_sovereign_agent/corpus/library/mod-playerbots
cd "$C" || exit 1

# A. Metric.h: io_context::work removed in Boost 1.90 -> executor_work_guard
sed -i 's|std::unique_ptr<boost::asio::io_context::work> m_queueServiceWork;|std::unique_ptr<boost::asio::executor_work_guard<boost::asio::io_context::executor_type>> m_queueServiceWork; // B1 fix cycle6 2026-09-29: io_context::work removed in Boost 1.90 (NetworkThread.hpp idiom)|' src/shared/Metric/Metric.h
sed -i 's|std::unique_ptr<boost::asio::io_context::work> m_writeServiceWork;|std::unique_ptr<boost::asio::executor_work_guard<boost::asio::io_context::executor_type>> m_writeServiceWork; // B1 fix cycle6 2026-09-29|' src/shared/Metric/Metric.h
grep -c 'executor_work_guard' src/shared/Metric/Metric.h

# B. Metric.cpp: reset(new work(...)) -> reset(new guard(make_work_guard(...)))
sed -i 's|m_queueServiceWork.reset(new boost::asio::io_context::work(m_queueService));|m_queueServiceWork.reset(new boost::asio::executor_work_guard<boost::asio::io_context::executor_type>(boost::asio::make_work_guard(m_queueService))); // B1 fix cycle6 2026-09-29|' src/shared/Metric/Metric.cpp
sed -i 's|m_writeServiceWork.reset(new boost::asio::io_context::work(m_writeService));|m_writeServiceWork.reset(new boost::asio::executor_work_guard<boost::asio::io_context::executor_type>(boost::asio::make_work_guard(m_writeService))); // B1 fix cycle6 2026-09-29|' src/shared/Metric/Metric.cpp
grep -c 'make_work_guard' src/shared/Metric/Metric.cpp

# C. WorldSession.cpp: address_v4::to_ulong removed -> to_uint (same uint32 value)
sed -i 's|make_address_v4(ip).to_ulong()|make_address_v4(ip).to_uint()|' src/game/Server/WorldSession.cpp
grep -c 'to_uint()' src/game/Server/WorldSession.cpp
echo "remaining io_context::work / to_ulong in tree: $(grep -rn 'io_context::work\|to_ulong' src/shared src/game src/mangosd src/realmd | grep -v 'was removed' | wc -l)"
echo ALL_CYCLE6_EDITS_DONE
