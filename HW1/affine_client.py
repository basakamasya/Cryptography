import requests # if this lib isn't installed yet --> pip install requests or pip3 intall requests

#Dont forget to open vpn
API_URL = 'http://10.36.52.109:5000' # ATTN: This is the current server (do not change unless being told so) 

if __name__ == '__main__':
    my_id = 44444	# ATTN: change this to your id number. it should be 5 digit number
    
    cipher_text = None
    letter = None

    endpoint = '{}/{}/{}'.format(API_URL, "affine_game", my_id )
    response = requests.get(endpoint) 	#get your ciphertext and most freq. letter
    if response.ok:	#if you get your ciphertext succesfully
        c = response.json()
        cipher_text = c[0]    #this is your ciphertext
        letter = c[1] 	#the most frequent letter in your plaintext

############ write decryption code for affine cipher here ##########




####################################################################

    elif(response.status_code == 404):
        print("We dont have a student with this ID. Check your id num")
    else:
        print("It was supposed to work:( Contact your TA")


#CHECK YOUR ANSWER HERE
    query = 'LOREM IPSUM FALAN FİLAN'	# ATTN: change this into the decrypted plaintext to be checked by the server. should be a string

    # Below is the sample code for sending your response back to the server
    endpoint = '{}/{}/{}/{}'.format(API_URL, "affine_game", my_id, query)
    response = requests.put(endpoint)
    if response.ok:
        c = response.json()
        print(c)
    elif (response.status_code == 404):
        print("check paramater types")
    elif(response.status_code == 406):
        print("Nope, Try again")
    elif(response.status_code == 401):
        print("Check your ID number")
    else:
        print("How did you get in here? Contact your TA")
