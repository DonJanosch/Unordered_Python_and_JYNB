import hashlib

def sha256(message,encoding='utf-8'):
    m =hashlib.sha256()
    m.update(str(message).encode(encoding))
    return int(m.hexdigest(),16)

Pcurve = 2**256 - 2**32 - 2**9 - 2**8 - 2**7 - 2**6 - 2**4 - 1 #Primenumber
N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCEAF48A03BBFD25E8CD0364141 #Group
Acurve = 0; Bcurve = 7 #Curve-Parameters for vizualization
Gx = 55066263022277343669578718895168534326250603453777594175500187360389116729240 #X-Coordinate of Generator-Point
Gy = 32670510020758816978083085130507043184471273380659243275938904335757337482424 #Y-Coordinate of Generator-Point
GPoint = (Gx,Gy) #Assembling the Generator-Point

#privKey = hex(123456789) #A random privat Key for testing purpouses
seed = 'Test2'
privKey = sha256(seed)%N
print('PrivKey {}'.format(privKey))

def modinv(a,n=Pcurve):
    lm,hm=1,0
    low, high = a%n,n
    while low >1:
        ratio = high/low
        nm,new=hm-lm*ratio, high-low*ratio
        lm, low, hm, high = nm, new, lm, low
    return lm %n

def ECadd(a,b):
    LamAdd = ((b[1]-a[1])*modinv(b[0]-a[0],Pcurve))%Pcurve
    x = (LamAdd*LamAdd-a[0]-b[0])%Pcurve
    y = (LamAdd*(a[0]-x)-a[1])%Pcurve
    return (x,y)

def ECdouble(a):
    Lam = ((3*a[0]*a[0]+Acurve)*modinv((2*a[1]),Pcurve))%Pcurve
    x = (Lam*Lam-2*a[0])%Pcurve
    y = (Lam*(a[0]-x)-a[1])%Pcurve
    return (x,y)

def EccMultiply(GenPoint,ScalarHex):
    if ScalarHex == 0 or ScalarHex >=N: raise Exception('Invalid Scalar/Private Key')
    ScalarBin = str(bin(ScalarHex))[2:]
    Q = GenPoint
    for i in range(1,len(ScalarBin)):
        Q=ECdouble(Q);
        print('DOU {}'.format(Q[0]))
        if ScalarBin[i] == '1':
            Q=ECadd(Q,GenPoint)
            print('ADD {}'.format(Q[0]))
    return (Q)

PublicKey = EccMultiply(GPoint,privKey)

print('PubKey:{}\nPrivKey:{}'.format(PublicKey[1],privKey))
