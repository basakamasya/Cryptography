# -*- coding: utf-8 -*-
"""hw1_q3_affine_cipher.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1gFQt4qKpbIhXLsHGWC9eLWS4haMsK2BE
"""

#Question 3
import requests  # if this lib isn't installed yet --> pip install requests or pip3 intall requests

# Dont forget to open vpn
API_URL = 'http://10.36.52.109:5000'  # ATTN: This is the current server (do not change unless being told so)

if __name__ == '__main__':
    my_id = 26628  # ATTN: change this to your id number. it should be 5 digit number

    cipher_text = None
    letter = None

    endpoint = '{}/{}/{}'.format(API_URL, "affine_game", my_id)
    response = requests.get(endpoint)  # get your ciphertext and most freq. letter
    if response.ok:  # if you get your ciphertext succesfully
        c = response.json()
        cipher_text = c[0]  # this is your ciphertext
        letter = c[1]  # the most frequent letter in your plaintext

    ############ write decryption code for affine cipher here ##########

        #taken from helper code
        # The extended Euclidean algorithm (EEA)
        def egcd(a, b):
            x, y, u, v = 0, 1, 1, 0
            while a != 0:
                q, r = b // a, b % a
                m, n = x - u * q, y - v * q
                b, a, x, y, u, v = a, r, u, v, m, n
            gcd = b
            return gcd, x, y
        # Modular inverse algorithm that uses EEA
        def modinv(a, m):
            if a < 0:
                a = m + a
            gcd, x, y = egcd(a, m)
            if gcd != 1:
                return None  # modular inverse does not exist
            else:
                return x % m
        # key object for Affine cipher
        # (alpha, beta) is the encryption key
        # (gamma, theta) is the decryption key
        class key(object):
            alpha = 0
            beta = 0
            gamma = 0
            theta = 0

        turkish_alphabet = {'A': 0, 'B': 1, 'C': 2, 'Ç': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'Ğ': 8, 'H': 9, 'I': 10,
                            'İ': 11, 'J': 12, 'K': 13, 'L': 14, 'M': 15, 'N': 16, 'O': 17, 'Ö': 18, 'P': 19,
                            'R': 20, 'S': 21, 'Ş': 22, 'T': 23, 'U': 24, 'Ü': 25, 'V': 26, 'Y': 27,
                            'Z': 28}

        inv_turkish_alphabet = {0: 'A', 1: 'B', 2: 'C', 3: 'Ç', 4: 'D', 5: 'E', 6: 'F', 7: 'G', 8: 'Ğ', 9: 'H',
                                10: 'I', 11: 'İ', 12: 'J', 13: 'K', 14: 'L', 15: 'M', 16: 'N', 17: 'O', 18: 'Ö',
                                19: 'P', 20: 'R', 21: 'S', 22: 'Ş', 23: 'T', 24: 'U', 25: 'Ü', 26: 'V',
                                27: 'Y', 28: 'Z'}
        #added
        turkish_alphabet_lower = {'a': 0, 'b': 1, 'c': 2, 'ç': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'ğ': 8, 'h': 9,
                                  'ı': 10,
                                  'i': 11, 'j': 12, 'k': 13, 'l': 14, 'm': 15, 'n': 16, 'o': 17, 'ö': 18, 'p': 19,
                                  'r': 20, 's': 21, 'ş': 22, 't': 23, 'u': 24, 'ü': 25, 'v': 26, 'y': 27,
                                  'z': 28}

        inv_turkish_alphabet_lower = {0: 'a', 1: 'b', 2: 'c', 3: 'ç', 4: 'd', 5: 'e', 6: 'f', 7: 'g', 8: 'ğ', 9: 'h',
                                      10: 'ı', 11: 'i', 12: 'j', 13: 'k', 14: 'l', 15: 'm', 16: 'n', 17: 'o', 18: 'ö',
                                      19: 'p', 20: 'r', 21: 's', 22: 'ş', 23: 't', 24: 'u', 25: 'ü', 26: 'v',
                                      27: 'y', 28: 'z'}


        # english alphabet decryption modified for turkish
        def Affine_Dec_Tr(ptext, key):
            plen = len(ptext)
            ctext = ''
            for i in range(0, plen):
                letter = ptext[i]
                if letter in turkish_alphabet_lower:
                    poz = turkish_alphabet_lower[letter]
                    poz = (key.gamma * poz + key.theta) % 29  # 29 letters in turkish alphabet
                    # print poz
                    ctext += inv_turkish_alphabet_lower[poz]
                elif letter in turkish_alphabet:
                    poz = turkish_alphabet[letter]
                    poz = (key.gamma * poz + key.theta) % 29
                    ctext += inv_turkish_alphabet[poz]
                else:
                    ctext += ptext[i]
            return ctext

        d = {} #for keeping the letter counts in the ciphertext to find the most frequent letter
        for i in cipher_text:
            if i not in d:
                d[i] = 1
            else:
                d[i] += 1
        #print(d)
        answer = ""
        for a in range(1, 29):  # since 29 is prime, every number smaller than 29 are relatively prime to 29
            key.alpha = a
            key.beta = 1 #since A-->0 corresponds to B-->1 beta should be 1
            key.gamma = modinv(key.alpha, 29)  # you can compute decryption key from encryption key
            key.theta = 29 - (key.gamma * key.beta) % 29

            #cipher_text = "MOIYJSBK CBZMBSTDSDKÜZMD ÖÜV MD KBÖBHCGJ İFKNZINTOKSBKMG ÖDU PÜKSÜÇHD ÇBAGH OTZBKÇDZ OTYZY ÇDCIÜRSDK RDKDŞD ÇBMDÖ ÇBSMGKGTOKSBKMG PNTNÇ PÜK CNKBÖÜ DSMDZ DSD MOSBRGTOK PBKMBÇSBKB PÜKB MOSMYKYSYTOKMY ÖÜVPÜKÜ UDZĞDKDMDZ ÜVDKÜ PBÇBZ ÖBTEBZSBKGZ RBRÇGZ TNJSDKÜZÜ ŞBKÇ DHIDIÜRHÜ ŞOXWOOM VÜŞHSÜAÜZÜZ CBÖÜPÜ PBT UÜSÇÜZİHOZ DSÜZMD PBKMBAG BTBAB ÇBSÇHG PÜKBJMBZ ÖDKÇDCÜ RDKDŞD ÇBMDÖ ÇBSMGKIBTB MBEDH DMDĞDAÜZÜ BIB MBÖB FZĞD PÜKÇBV CFJ DHIDTÜ İFKDE PÜSMÜAÜZÜ CFTSDMÜ YJYZ CNKDZ PÜK İNEDZCÜJSÜÇ ED BZSBRIBJSGÇ MFZDIÜZÜZ BKHGÇ COZB DKIÜR OSIBCG ÇDZMÜCÜ ED ÖÜV ÇYRÇYCYJ OKBMB PYSYZBZ ÖDKÇDC ÜVÜZ PNTNÇ PÜK IYHSYSYÇ ÇBTZBAGTMG ÇOIRY VÜŞHSÜÇSDKMDÇÜ ÜZCBZSBK ÖBTEBZ VÜŞHSÜAÜZÜZ CBTİGMDADK CBÖÜUSDKÜZD PÜK CNKD MNRIBZSGÇ MYTİYSBKGTSB MDAÜSCD MD ÇYRÇYTSB TBÇSBRIGRSBKMG BIB ÇDZMÜCÜ ED OKBMB PYSYZBZSBK ÜZCBZSBKGZ PY ÇYRÇYĞY TBÇSBRGIGZG PÜSD UBTSBRIBIGRSBKMG"

            plain = Affine_Dec_Tr(cipher_text, key)
            print("When alpha is", a, "and beta is", 1, ":", plain)
            if a == 18:
                answer = plain
                #print(answer)

    ####################################################################

    elif (response.status_code == 404):
        print("We dont have a student with this ID. Check your id num")
    else:
        print("It was supposed to work:( Contact your TA")

    # CHECK YOUR ANSWER HERE
    query = answer  # ATTN: change this into the decrypted plaintext to be checked by the server. should be a string

    # Below is the sample code for sending your response back to the server
    endpoint = '{}/{}/{}/{}'.format(API_URL, "affine_game", my_id, query)
    response = requests.put(endpoint)
    if response.ok:
        c = response.json()
        print(c)
    elif (response.status_code == 404):
        print("check paramater types")
    elif (response.status_code == 406):
        print("Nope, Try again")
    elif (response.status_code == 401):
        print("Check your ID number")
    else:
        print("How did you get in here? Contact your TA")