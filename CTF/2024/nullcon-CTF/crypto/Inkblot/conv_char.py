pem = open("ecdsa_test").read()
open("ecdsa_test_conv", "w").write(pem.replace("*", "A"))
