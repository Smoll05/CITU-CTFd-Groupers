## Challenge Name: LSB - Blue in the image  
Category: MISC  
Points: 150  

### Challenge Description:  
We are given an image file with no visible flag or hints. However, the name of the challenge and behavior of the image suggest LSB (Least Significant Bit) steganography, particularly targeting the blue channel.


### Approach

**1. Using zsteg to extract LSB data from the blue channel**

We ran the image through the `zsteg` tool, a popular tool for steganography analysis. Using the command:

```
zsteg -a <image>
```

we found a hidden message embedded in the LSB of the blue channel.

**2. Alternatively, using online OSINT tools like [aperisolve.fr](http://aperisolve.fr)**

![Aperi ZSteg](https://raw.githubusercontent.com/Smoll05/CITU-CTFd-Groupers/main/Writeup-Images/lsb-zsteg.png)


A simpler approach was to upload the image to Aperisolve, which also runs LSB analysis. The flag was visible in the extracted text section.

```
CITU{LSBEmbedOnBlue_Channel}
```

[**Back to Home**](/)