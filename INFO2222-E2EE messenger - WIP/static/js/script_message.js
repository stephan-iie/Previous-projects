//PLEASE NOTE: THIS IS JUST USED FOR TESTING, SUBJECT TO CHANGE
  //gets recently registered username 

  document.onload=check();
  let ciphertext;
  let iv;

  //addFriend so we have potential friend to add
  
  // Onload function 
  async function check(){
      // Check who we are talking to 
      var recipient = getCookie("currentChat");
      var extracted = getCookie("secretExtracted");
  
      var extractedSecret =getCookie("secret"); // do we still need this?
  
      var signedSecret =getCookie("secretSigned");
      var encryptedSecret =getCookie("secretEncrypted");
  
      if (recipient=="Server"){
          // We dont need to do anything if its the server, nothing to decrypt or anything liek that 
          console.log("No friend rn, not doing anything")
          return;

      } else {
          // Extracting secret key IF we have one 
          console.log("Number of messages",  (document.getElementById('messages').childNodes.length-1)/2)

          // If there is no indicatiton of secret NOR extraction status 
          if (extracted=="" &&  signedSecret=="" &&  encryptedSecret==""){
              console.log("There is no secrt to decrypt and verify yet")
              //return;
  
              // TO DO: extract, decrpy 
  
            // If the extrated cookie has not been set but we have a secret -> we are the first to generate the secret, reload the page to send back to server
          } else if(extracted=="" &&  signedSecret!="" &&  encryptedSecret!="") {
              // if extraction status is false  -> we need to extract the secret 
              console.log("RELOADING PAGE");
              window.location.reload(true);
  
          } else if (extracted=="False" ){
              console.log("Starting to decrpt and verify")
              
              // Convert the secrets to the appropriate format
              signedSecret = base64StringToArrayBuffer(getCookie("secretSigned").slice(1, -1));
              encryptedSecret = base64StringToArrayBuffer(getCookie("secretEncrypted").slice(1, -1));
  
              alert("importing keys ")
              // Import the friends Signing key for verification 
              console.log(getCookie("friendKeySv").slice(1, -1))
              var verifyCookie = base64StringToArrayBuffer(getCookie("friendKeySv").slice(1, -1));
              var friendVerify= await window.crypto.subtle.importKey(
                  "spki",
                  verifyCookie,
                  {
                  name: "RSASSA-PKCS1-v1_5",
                  hash: "SHA-256"
                  },
                  true,
                  ["verify"]
              );
  
              alert("Starting decrypt and verify ")
          // Decrypt the enrypted secret by using clients private key 
              
              callOnStore(function (store) {
                  console.log(getCookie("user")+"ed");
                  var getData = store.get(getCookie("user")+"ed"); // NEED TO INDICTE WHCIH KEY WHEN EXTRATING NO W
              
                  getData.onsuccess = async function() {
                    var keys = getData.result.keys;
                    console.log(keys)
                    console.log("starting decryption");
                    console.log(encryptedSecret);
                    //decrypting  
                  
                    let decrypted =   await window.crypto.subtle.decrypt(
                          {
                          name: "RSA-OAEP"
                          },
                          keys.privateKey,
                          encryptedSecret
                      );
  
                    console.log("The resulting secret", arrayBufferToBase64String(decrypted))
                    alert("Decrypted")
  
                    // Verify the signed secret by using the friends PublicKeySv
  
                    let result = await window.crypto.subtle.verify(
                      "RSASSA-PKCS1-v1_5",
                      friendVerify,
                      signedSecret,
                      decrypted 
                    );
                  // Save it in the secret cookie if it does exist 
                    if (result==true){
                      console.log("verified")
                      document.cookie="secret="+arrayBufferToBase64String(decrypted);
                      document.cookie="secretExtracted=True"
                    }else{
                      console.log("error with secret key")
                    }       
                  }
              
              })
  
          // If we do have a secret -> decrypt stuff -> can remove this now that decryptio os below 
          }else {
              console.log(extractedSecret)
          }


          // check if there are messages to decrypt =====================================================   
          // Get the secret key
          if ((document.getElementById("messages").childNodes.length-1)/2 > 0 ){
            console.log("Decrytpion started...")
            // Get the cipher text list
            let cipher = document.getElementById("messages").value


            // Get the iv
            //console.log(cipher.split(/\r?\n/)[0].split(" ")[1])
           
            // Iteriate through the list
            /*for (let i = 0; i < cipher.length; i++) {
              // Iteriate through the dictionary
              for (const [key, value] of Object.entries(cipher[i])) {
                console.log(key, value);
              }
            }*/
            
            
            /*const dec = await msgdecryption(cipher[0], civ)
            console.log("decMsg: ", dec)
            console.log("HMAC checking test...")
            let hmacS = dec.split(",")[1]
            console.log("received HMAC signature: ", hmacS)
            console.log("Start verifying HMAC...")
            let msgS = dec.split(",")[0]
            // Verify signature
            if (await verifySignature(msgS, hmacS, secret) == true) {
              // Display msg
              return msgS
            } else {
              // Warning
              return "An attacker has modified your msg!"
            }*/
          }
          // ===================================================================================================  
          // For each friend -> retrieve the key and decrypt the messages (only need to decrypt friends messages!) use the class selector friend_messages
  
      }
  }
  
  function textToArrayBuffer(str) {
      var buf = unescape(encodeURIComponent(str)) // 2 bytes for each char
      var bufView = new Uint8Array(buf.length)
      for (var i=0; i < buf.length; i++) {
        bufView[i] = buf.charCodeAt(i)
      }
      return bufView
    }
  
  function arrayBufferToText(arrayBuffer) {
    var byteArray = new Uint8Array(arrayBuffer)
    var str = ''
    for (var i=0; i<byteArray.byteLength; i++) {
      str += String.fromCharCode(byteArray[i])
    }
    return str
  }
  
  function arrayBufferToBase64String(arrayBuffer) {
    var byteArray = new Uint8Array(arrayBuffer)
    var byteString = ''
    for (var i=0; i<byteArray.byteLength; i++) {
      byteString += String.fromCharCode(byteArray[i])
    }
    return btoa(byteString)
  }
  
  function base64StringToArrayBuffer(b64str) {
    var byteStr = window.atob(b64str)
    var bytes = new Uint8Array(byteStr.length)
    for (var i = 0; i < byteStr.length; i++) {
      bytes[i] = byteStr.charCodeAt(i)
    }
    return bytes.buffer
  }

// ===================================================================================================
// Functions to "Sign & Verify" the messages using HMAC: activated when the message button is clicked
// HMAC(key, message)
// Used code from: https://bradyjoslin.com/blog/hmac-sig-webcrypto/
// Function for generating crypto key based on the shared secret key.
// The crypto key will be used for sign and verify functions.
/*const result = crypto.subtle.importKey(
            format, // raw format
            keyData, // shared secret encoded as an Uint8Array
            algorithm,
            extractable,
            usages // lalow the key to be used for both signing and verifying.
    );
 */
// Get the secret key
const secret = getCookie("secret"); 

// Get crypto key for HMAC
async function importKey(secret) {
  return await crypto.subtle.importKey(
    'raw',
    new TextEncoder().encode(secret),
    { name: 'HMAC', hash: 'SHA-256' },
    false,
    ['sign', 'verify'],
  )
}

// https://stackoverflow.com/a/11058858
function str2ab(str) {
  const buf = new ArrayBuffer(str.length);
  const bufView = new Uint8Array(buf);
  for (let i = 0, strLen = str.length; i < strLen; i++) {
    bufView[i] = str.charCodeAt(i);
  }
  return buf;
}

// Get crypto key for AES-GCM encryption
async function importSessionKey() {
  // Get the secret key
  const secret = getCookie("secret"); 
  var key = await crypto.subtle.importKey(
    "raw",
    //str2ab("1234567890123456"),
    base64StringToArrayBuffer(secret),
    { name: "AES-GCM" },
    true,
    ['encrypt', 'decrypt']
  );
  return key;
}

// Function for deriving signatures. (in base64 format)
// Accept message and secret as string
// Use the Web Crypto sign() method to create the signature,
// const signature = crypto.subtle.sign(algorithm, key, data);
async function signResponse(message, secret) {
  console.log("start HMAC")
  const key = await importKey(secret);
  const signature = await crypto.subtle.sign(
    'HMAC',
    key,
    // Convert str(message) to ArrayBuffer type
    new TextEncoder().encode(message),
  )
  // Convert ArrayBuffer to Base64
  return btoa(String.fromCharCode(...new Uint8Array(signature)));
}


// Function for verifying the HMAC signature
// const result = crypto.subtle.verify(algorithm, key, signature, data)
async function verifySignature(message, signature, secret) {
  const key = await importKey(secret);

  // Convert Base64 to Uint8Array
  const sigBuf = Uint8Array.from(atob(signature), c => c.charCodeAt(0));

  return await crypto.subtle.verify(
    'HMAC',
    key,
    sigBuf,
    new TextEncoder().encode(message),
  );
}

// Encryption & decryption of messages -> https://github.com/mdn/dom-examples/blob/master/web-crypto/encrypt-decrypt/aes-cbc.js
// HMAC -> https://bradyjoslin.com/blog/hmac-sig-webcrypto/
  
// Get the message
function getMessage() {
  console.log("Getting msg")
  let message = document.getElementById("messageInput").value
  // DELETE IT LATER =========================================================================
  console.log("msg:", message)
  // DELETE IT LATER =========================================================================

  return message;
}

// Sign and encrypt the message date & time
async function timeencryption() {
  console.log("Getting current date")
  var x = Date()
  console.log("Current Date: ", x)

  // Generate HMAC 
  const hmac = await signResponse(x, secret);
  const msgTime = [x, hmac];

  // DELETE IT LATER =========================================================================
  console.log("Time HMAC:", hmac);
  // DELETE IT LATER =========================================================================

  console.log("Time encryption started")
  const key = await importSessionKey()
  let cipherTime = await window.crypto.subtle.encrypt(
    {
      name: "AES-GCM",
      iv
    },
    key,
    new TextEncoder().encode(msgTime)
  );
  return cipherTime;
}

// Function to encrypt the message + HMAC signature.
// Encryption(key, message || HMAC)
async function msgencryption() {
  // Get the message in the textbox
  let msgs = getMessage();
  iv = window.crypto.getRandomValues(new Uint8Array(8));

  // Generate HMAC 
  const hmac = await signResponse(msgs, secret);

  // DELETE IT LATER =========================================================================
  console.log("HMAC:", hmac);
  // DELETE IT LATER =========================================================================

  const msg = [msgs, hmac];

  // DELETE IT LATER =========================================================================
  console.log("msg:", msg)
  // DELETE IT LATER =========================================================================
  
  console.log("encryption started")
  const key = await importSessionKey()
  let ciphertext = await window.crypto.subtle.encrypt(
    {
      name: "AES-GCM",
      iv
    },
    key,
    new TextEncoder().encode(msg)
  );

  // DELETE IT LATER =========================================================================
  console.log("Encrypted Msg", ciphertext)
  
  // Get the encrypted time
  let enTime = await timeencryption()

  // DELETE IT LATER =========================================================================
  console.log("Encrypted Time:", enTime);
  // DELETE IT LATER =========================================================================

  let cipher = new FormData();
  cipher.append('CMsg', arrayBufferToBase64String(ciphertext));
  cipher.append('IV', arrayBufferToBase64String(iv));
  cipher.append('msgTime', arrayBufferToBase64String(enTime));
  
  // DELETE IT LATER =========================================================================

  /*const ciphertextValue = document.querySelector(".aes-cbc .ciphertext-value");
  ciphertextValue.classList.add('fade-in');
  ciphertextValue.addEventListener('animationend', () => {
    ciphertextValue.classList.remove('fade-in');
  });
  ciphertextValue.textContent = `${buffer}...[${ciphertext.byteLength} bytes total]`;*/

  // Send the encrypted string to server
  fetch('/displayMessage', {
    method: 'POST',
    body: cipher
  }).then(function() {
  });
  //document.getElementById("ciphertext").innerHTML = "CMsg"

  return true;
}


// Function for verify HMAC & decryption
async function msgdecryption(ciphertext, iv) {
  // Get the key
  var sessionKey = await importSessionKey()

  let decrypted = await window.crypto.subtle.decrypt(
    {
      name: "AES-GCM",
      iv
    },
    sessionKey,
    ciphertext
  );

  /* DELETE IT LATER =========================================================================
  console.log("decMsg:", decrypted);
  // DELETE IT LATER =========================================================================*/

  /*let dec = new TextDecoder();
  const decryptedValue = document.querySelector(".aes-cbc .decrypted-value");
  decryptedValue.classList.add('fade-in');
  decryptedValue.addEventListener('animationend', () => {
    decryptedValue.classList.remove('fade-in');
  });

  const isSigValid = await verifySignature(message, signature, secret)
  decryptedValue.textContent = dec.decode(decrypted);*/

  // Convert Array buffer to string 
  let decMsg = new TextDecoder("utf-8").decode(decrypted);
  return decMsg;
}
// ==============================================================================================

  
  
  // function to transmit if clicking message friend button: activated when the chatwith button for friend is called (assume for now the script is called before the post request sent)
  async function newChat(button){ //use button.value to extract name of person chattingwith 
      var extracted = getCookie("secretExtracted"); // gets the secret for the specific 
  
  
      // Check if there already is a shared secret cookie (get the server to set one for both ends -> retrieve from database if exists when click chat with and put in cookie )
      if (extracted!=""){//check
          console.log("There is a secret and we have extracted it or are extracting, dont do anything, dont need to generate a new secrt ")
  
      }else{ // There is no shared secret, you are the first to generate the secret so generate ths secret and send ti 
  
      //Generate a random symmetric key -> TO DO: change later for now just use readable so we know 
      var secret = makeData();
      console.log("secret: ", arrayBufferToBase64String(secret));
      document.cookie="secret=" + arrayBufferToBase64String(secret);
      /*
      var secret = await window.crypto.subtle.generateKey(
        {
          name: "AES-CBC",
          length: 256
        },
        true,
        ["encrypt", "decrypt"]
      ).then((keyPair) => {
        expp(keyPair);
      })

      async function expp(keyPair){
        var exported = await window.crypto.subtle.exportKey(
          "raw",
          keyPair
        );
        console.log(secret)
        console.log(exported)
        const exportedAsString = ab2str(exported);
        console.log(exportedAsString)
        const exportedAsBase64 = window.btoa(exportedAsString);
        console.log("secret: ", exportedAsBase64);
        document.cookie="secret=" + exportedAsBase64;

      }
      */
      
      function ab2str(buf) {
        return String.fromCharCode.apply(null, new Uint8Array(buf));
      }

      
      //--> TO DO: keep this, but in server, if secret key exists and retrieved = false, reset the person retrieving key secret cookie to nothing 
      // Need database to keep track of whos extracted or not -> if sent in , indicate extracted DONT resent secret cookie. IF not the one who stored it, remove secret cookie 
  
      //Extract the friends public key from the cookie : TO DO: change to actual cookie -> passed when friend is added
      //console.log( getCookie("friendKeyEd").slice(1, -1))
      var binaryDer = base64StringToArrayBuffer(  getCookie("friendKeyEd").slice(1, -1)) //
     // const binaryDerString = window.atob(getCookie("friendKeyEd"));
      //const binaryDerString = str2ab(binaryDer);
  
      alert("importing friend key ")
  
      //Import the friends public key
      var friendKey= await window.crypto.subtle.importKey(
          "spki",
          binaryDer,
          {
            name: "RSA-OAEP",
            hash: "SHA-256"
          },
          true,
          ["encrypt"]
        );
  
      alert(friendKey);
  
      //sign the secret key, store in a cookie for server
         callOnStore(function (store) {
          console.log(getCookie("user")+"sv");
          var getData = store.get(getCookie("user")+"sv"); // NEED TO INDICTE WHCIH KEY WHEN EXTRATING NO W
        
          getData.onsuccess = async function() {
          var keys = getData.result.keys;
          console.log("getting signed");
  
          console.log(keys)
          
          //signing 
          let signature =   await window.crypto.subtle.sign(
              "RSASSA-PKCS1-v1_5",
              keys.privateKey, // retrieves the secret key 
              secret
          );
  
          console.log(arrayBufferToBase64String(signature))
         document.cookie="secretSigned="+arrayBufferToBase64String(signature);
  
           //Encrypt the symmetric key  and store in cookie for server
          let encryption =   await window.crypto.subtle.encrypt(
              {
                  name: "RSA-OAEP"
                },
                friendKey,
                secret
          );
          document.cookie="secretEncrypted="+arrayBufferToBase64String(encryption);
          
  
          //debugging 
          console.log("sig:", arrayBufferToBase64String(signature));
          console.log("enc:", arrayBufferToBase64String(encryption));
         };
          })
  
  
  
      }
          
  
      return true;
  
  }
  
  
  
  // Generates random values for secret 
  function makeData() {
    return window.crypto.getRandomValues(new Uint8Array(16))
  }
  
  
  
  async function retreiveKey(type){
      var k=await loadKeyDecryptData(type);
      return k;
  }
  
    function getCookie(cname) {
      let name = cname + "=";
      let decodedCookie = decodeURIComponent(document.cookie);
      let ca = decodedCookie.split(';');
      for(let i = 0; i <ca.length; i++) {
        let c = ca[i];
        while (c.charAt(0) == ' ') {
          c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
          return c.substring(name.length, c.length);
        }
      }
      return "";
    }
  
  
    // Stores key
    async function encryptDataSaveKey(keys) {
      callOnStore(function (store) {
        store.put({username: getCookie("potential_username"), keys: keys});
      })
    }
  
    // gets key 
    function loadKeyDecryptData(type) {
      callOnStore(function (store) {
          console.log(getCookie("user")+type);
        var getData = store.get(getCookie("user")+type); // NEED TO INDICTE WHCIH KEY WHEN EXTRATING NO W
        getData.onsuccess = async function() {
          var keys = getData.result.keys;
          console.log("key:", keys);
         };
      })
    }
  
  /*index db storing unctions*/
    function callOnStore(fn_) {
  
      // This works on all devices/browsers, and uses IndexedDBShim as a final fallback 
      var indexedDB = window.indexedDB || window.mozIndexedDB || window.webkitIndexedDB || window.msIndexedDB || window.shimIndexedDB;
  
      // Open (or create) the database
      var open = indexedDB.open("MyDatabase", 1);
  
      // Create the schema if needed 
      open.onupgradeneeded = function() {
          var db = open.result;
          var store = db.createObjectStore("MyObjectStore", {keyPath: "username"});
      };
  
      // If we can open it 
      open.onsuccess = function() {
          // Start a new transaction
          var db = open.result;
          var tx = db.transaction("MyObjectStore", "readwrite");
          var store = tx.objectStore("MyObjectStore");
  
          // depends on the function passed 
          fn_(store)
  
  
          // Close the db when the transaction is done
          tx.oncomplete = function() {
            console.log("completed function");
              db.close();
          };
      }
  
  
  
    }