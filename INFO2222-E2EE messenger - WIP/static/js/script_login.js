document.onload=register();

 async function register(){
    /*implement adding public private key and sending during registration*/
    console.log("You clicked Register");

    "use strict";
    if (!window.crypto || !window.crypto.subtle) {
        alert("Your current browser does not support the Web Cryptography API! This page will not work.");
        return;
    }
    // All the work happens here.
    alert("starting processing");

    /*
Convert  an ArrayBuffer into a string
from https://developer.chrome.com/blog/how-to-convert-arraybuffer-to-and-from-string/
*/
function ab2str(buf) {
  return String.fromCharCode.apply(null, new Uint8Array(buf));
}

  //gets recently registered username 

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
  async function encryptDataSaveKey(keys, type) {
    callOnStore(function (store) {
      store.put({username: getCookie("potential_username")+type, keys: keys});
    })
  }

  // gets key 
  function loadKeyDecryptData() {
    callOnStore(function (store) {
      var getData = store.get(getCookie("user"));
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

/*
Export the given key and write it into the "exported-key" space.
*/
async function exportCryptoKey(key, type) {
  const exported = await window.crypto.subtle.exportKey(
    "spki",
    key
  );
  const exportedAsString = ab2str(exported);
  const exportedAsBase64 = window.btoa(exportedAsString);
  const pemExported = `-----BEGIN PUBLIC KEY-----\n${exportedAsBase64}\n-----END PUBLIC KEY-----`;
  document.cookie= type +"="+exportedAsBase64+";path=/" ;
  console.log(type+ exportedAsBase64)
}

/*
Generate an encrypt/decrypt key pair,
then set up an event listener on the "Export" button.
*/
window.crypto.subtle.generateKey(
  {
    name: "RSA-OAEP",
    // Consider using a 4096-bit key for systems that require long-term security
    modulusLength: 2048,
    publicExponent: new Uint8Array([1, 0, 1]),
    hash: "SHA-256",
  },
  true,
  ["encrypt", "decrypt"]
).then((keyPair) => {
  /* CHANGE LATER TO INCLUDE USR PKEY!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!*/
   /* document.cookie="PrivateKey="+keyPair.privateKey+";path=/";*/
    const pubkey=  exportCryptoKey(keyPair.publicKey, "PublicKeyEd");
    console.log("done exporting pkey as cookie, now sotirng in indexdb");

    encryptDataSaveKey(keyPair, "ed");

});

alert("generating signing key ");
// Generate signing keys
window.crypto.subtle.generateKey(
  {
    name: "RSASSA-PKCS1-v1_5",
      hash: {
        name: "SHA-256"
      },
      modulusLength: 2048,
      extractable: false,
      publicExponent: new Uint8Array([1, 0, 1])
  },
  true,
  ["sign", "verify"]
).then((keyPair) => {
  /* CHANGE LATER TO INCLUDE USR PKEY!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!*/
   /* document.cookie="PrivateKey="+keyPair.privateKey+";path=/";*/
    const pubkey=  exportCryptoKey(keyPair.publicKey, "PublicKeySv");
    console.log("done exporting pkey as cookie, now sotirng in indexdb");
    encryptDataSaveKey(keyPair, "sv");

});


    alert("fin");

    return;

}
