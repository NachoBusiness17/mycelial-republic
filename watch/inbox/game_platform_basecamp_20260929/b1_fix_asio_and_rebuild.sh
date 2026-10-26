#!/bin/bash
# B1 build fix: Boost 1.90 removed asio::io_service (typedef-era API) -> io_context
cd ~/mangos-wotlk || exit 1
echo "=== files patched ==="
grep -rl 'boost::asio::io_service' src/ | tee /tmp/asio_files.txt
xargs -r sed -i 's/boost::asio::io_service/boost::asio::io_context/g' < /tmp/asio_files.txt
echo "=== rebuild ==="
cd build && make -j12 2> /tmp/make_err.log | tail -20
echo "MAKE_EXIT=${PIPESTATUS[0]}"
tail -5 /tmp/make_err.log
