"""

  Licensed to the Apache Software Foundation (ASF) under one
  or more contributor license agreements.  See the NOTICE file
  distributed with this work for additional information
  regarding copyright ownership.  The ASF licenses this file
  to you under the Apache License, Version 2.0 (the
  "License"); you may not use this file except in compliance
  with the License.  You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.
"""
# Instructions:
# 1. Run Thrift to generate the python module hbase
#    thrift --gen py ../../../../../hbase-thrift/src/main/resources/org/apache/hadoop \
#      /hbase/thrift2/hbase.thrift
# 2. Create a directory of your choosing that contains:
#     a. This file (DemoClient.py).
#     b. The directory gen-py/hbase (generated by instruction step 1).
# 3. pip install thrift==0.9.3
# 4. Create a table call "example", with a family called "family1" using the hbase shell.
# 5. Start the hbase thrift2 server
#    bin/hbase thrift2 start
# 6. Execute {python DemoClient.py}.

import sys
import os
import time

from thrift.transport import TTransport
from thrift.transport import TSocket
from thrift.transport import THttpClient
from thrift.protocol import TBinaryProtocol
from thrift.protocol import TCompactProtocol

# Add path for local "gen-py/hbase" for the pre-generated module
gen_py_path = os.path.abspath('gen-py')
sys.path.append(gen_py_path)
from hbase import THBaseService
from hbase.ttypes import *

print("Thrift2 Demo")
print("This demo assumes you have a table called \"example\" with a column family called \"family1\"")

LINE_DOMAIN = "http://cnndcphad005.kaiser.org"
LINE_HTTP_URL = LINE_DOMAIN + "/api/v4/TalkService.do"

host = "cnndcphad005.kaiser.org"
port = 9090
framed = True

# Make socket
transport = TSocket.TSocket(host, port)

# Buffering is critical. Raw sockets are very slow
transport = TTransport.TBufferedTransport(transport)

# Wrap in a protocol
protocol = TBinaryProtocol.TBinaryProtocol(transport)

# Create a client to use the protocol encoder
client = THttpClient.THttpClient(protocol)

transport.open()

table = "example"

put = TPut(row="row1", columnValues=[TColumnValue(family="family1",qualifier="qualifier1",value="value1")])
print("Putting:", put)
client.put(table, put)

get = TGet(row="row1")
print("Getting:", get)
result = client.get(table, get)

print("Result:", result)

transport.close()
