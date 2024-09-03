# Network_protocols
 demo

 # QUIC demo:

Go to folder "QUIC"
 For sever run in bash:
 python examples/http3_server.py --certificate tests/ssl_cert.pem --private-key tests/ssl_key.pem --port 8053


 For demo run in bash:
 uvicorn demo:app --host 127.0.0.1 --port 8053

Go to address 127.0.0.1:8053