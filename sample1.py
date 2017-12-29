import datetime
import traceback

from charm.core.engine.util import objectToBytes,bytesToObject

from charm.toolbox.pairinggroup import PairingGroup
from charm.schemes.abenc.abenc_bsw07 import CPabe_BSW07
from charm.adapters.abenc_adapt_hybrid import HybridABEnc 

debug = True

groupObj = PairingGroup('SS512')
cpabe = CPabe_BSW07(groupObj)
hybrid_abe = HybridABEnc(cpabe, groupObj)

access_policy = '(SYSADMIN and SECURITYTEAM) or (BUSINESSSTAFF and ((executivelevel7 and auditgroup) or (executivelevel7 and strategyteam) or (auditgroup and strategyteam)))'
data = "hello world this is an important message. encounter in string format"
data = bytes(data, 'utf-8')
(pk, mk) = hybrid_abe.setup()
if debug: print("pk => ", str(objectToBytes(pk,groupObj), 'utf-8'))
if debug: print("mk => ", str(objectToBytes(mk,groupObj), 'utf-8'))

# print(type(data), data)
# print(access_policy)
ciphertext = hybrid_abe.encrypt(pk, data, access_policy)
ciphertext = objectToBytes(ciphertext,groupObj)
print("ciphertext: ", ciphertext)

sara_attributes = ['SYSADMIN', 'ITDEPARTMENT']
kevin_attributes = ['BUSINESSSTAFF', 'STRATEGYTEAM', 'EXECUTIVELEVEL7']

print(sara_attributes)
print(kevin_attributes)

sara_sk = hybrid_abe.keygen(pk, mk, sara_attributes)
sara_sk = objectToBytes(sara_sk, groupObj)
if debug: print("sara_sk => ", sara_sk)

kevin_sk = hybrid_abe.keygen(pk, mk, kevin_attributes)
kevin_sk = objectToBytes(kevin_sk, groupObj)
if debug: print("kevin_sk => ", kevin_sk)

try:
    sara_plaintext = hybrid_abe.decrypt(pk, 
                                        bytesToObject(sara_sk,groupObj), 
                                        bytesToObject(ciphertext,groupObj))
    if debug: print("sara_plaintext: " + str(sara_plaintext))
    assert sara_plaintext != data
except Exception as e:
    print("Sara can't decrypt ciphertext")
    traceback.print_exc()
finally:
    print("Decrypting using Sara's private key finished")

try:
    kevin_plaintext = hybrid_abe.decrypt(pk, 
                                         bytesToObject(kevin_sk,groupObj), 
                                         bytesToObject(ciphertext,groupObj))
    if debug: print("kevin_plaintext: " + str(kevin_plaintext,'utf-8'))
    assert kevin_plaintext == data
except Exception as e:
    print("Kevin can't decrypt ciphertext")
    traceback.print_exc()
finally:
    print("Decrypting using Kevin's private key finished")
