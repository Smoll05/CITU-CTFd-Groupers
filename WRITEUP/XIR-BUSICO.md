## Challenge Name: XIR BUSICO  
Category: Cryptography
Points: 150  
Solves: 17  

### Challenge Description:  
**What I am drinking now? a COFFEE or WATER?**

We are given an encoded string:

```
T7a6WYSMbYyHb6CNfoaeeJCxbYyxZYuxZYyT
```
---

### Approach

**1. Initial analysis - Base64 suspicion**

The structure of the string suggested it might be base64-encoded. Decoding it from base64 gave us a binary-like output, but it wasn’t human-readable.

**2. XOR Cipher - Guided by the clue**

Based on the title “XIR BUSICO” and the description referencing “COFFEE or WATER?”, we guessed it was a **XOR cipher**. The keyword "COFFEE" stood out as both a pun and a potential hexadecimal value for the key.

We converted the ASCII string `COFFEE` into its hex representation:

```
C0 FF EE
```

Then we used this as the key for XORing the decoded base64 content. After applying the XOR operation, we revealed the flag:

```
CITU{basic_crypto_as_it_is}
```

[**Back to Home**](/)