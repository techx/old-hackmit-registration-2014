/*
 *
 *  Secure Hash Algorithm (SHA256)
 *  http://www.happycode.info/
 *
 *  Some functions taken from http://jssha.sourceforge.net/
 *
 */

function SHA224(str) {

  var H = [0xc1059ed8, 0x367cd507, 0x3070dd17, 0xf70e5939, 0xffc00b31, 0x68581511, 0x64f98fa7, 0xbefa4fa4];
  var K = [0x428A2F98, 0x71374491, 0xB5C0FBCF, 0xE9B5DBA5, 0x3956C25B, 0x59F111F1, 0x923F82A4, 0xAB1C5ED5,
    0xD807AA98, 0x12835B01, 0x243185BE, 0x550C7DC3, 0x72BE5D74, 0x80DEB1FE, 0x9BDC06A7, 0xC19BF174,
    0xE49B69C1, 0xEFBE4786, 0xFC19DC6, 0x240CA1CC, 0x2DE92C6F, 0x4A7484AA, 0x5CB0A9DC, 0x76F988DA,
    0x983E5152, 0xA831C66D, 0xB00327C8, 0xBF597FC7, 0xC6E00BF3, 0xD5A79147, 0x6CA6351, 0x14292967,
    0x27B70A85, 0x2E1B2138, 0x4D2C6DFC, 0x53380D13, 0x650A7354, 0x766A0ABB, 0x81C2C92E, 0x92722C85,
    0xA2BFE8A1, 0xA81A664B, 0xC24B8B70, 0xC76C51A3, 0xD192E819, 0xD6990624, 0xF40E3585, 0x106AA070,
    0x19A4C116, 0x1E376C08, 0x2748774C, 0x34B0BCB5, 0x391C0CB3, 0x4ED8AA4A, 0x5B9CCA4F, 0x682E6FF3,
    0x748F82EE, 0x78A5636F, 0x84C87814, 0x8CC70208, 0x90BEFFFA, 0xA4506CEB, 0xBEF9A3F7, 0xC67178F2];
  var W = new Array(64);
  var a, b, c, d, e, f, g, h, i, j;
  var T1, T2;
  var charsize = 8;

  function utf8_encode(str) {
    return unescape(encodeURIComponent(str));
  }

  function str2binb(str) {
    var bin = [];
    var mask = (1 << charsize) - 1;
    var len = str.length * charsize;

    for (var i = 0; i < len; i += charsize) {
      bin[i >> 5] |= (str.charCodeAt(i / charsize) & mask) << (32 - charsize - (i % 32));
    }

    return bin;
  }

  function binb2hex(binarray) {
    var hex_tab = '0123456789abcdef';
    var str = "";
    var len = binarray.length * 4;
    var srcByte;

    for (var i = 0; i < len-1; i += 1) { // omit H7
      srcByte = binarray[i >> 2] >> ((3 - (i % 4)) * 8);
      str += hex_tab.charAt((srcByte >> 4) & 0xF) + hex_tab.charAt(srcByte & 0xF);
    }

    return str;
  }

  function safe_add_2(x, y) {
    var lsw = (x & 0xFFFF) + (y & 0xFFFF);
    var msw = (x >>> 16) + (y >>> 16) + (lsw >>> 16);

    return ((msw & 0xFFFF) << 16) | (lsw & 0xFFFF);
  }

  function maj(x, y, z) {
    return (x & y) ^ (x & z) ^ (y & z);
  }

  function ch(x, y, z) {
    return (x & y) ^ (~x & z);
  }

  function rotr(x, n) {
    return (x >>> n) | (x << (32 - n));
  }

  function shr(x, n) {
    return x >>> n;
  }

  function sigma0(x) {
    return rotr(x, 2) ^ rotr(x, 13) ^ rotr(x, 22);
  }

  function sigma1(x) {
    return rotr(x, 6) ^ rotr(x, 11) ^ rotr(x, 25);
  }

  function gamma0(x) {
    return rotr(x, 7) ^ rotr(x, 18) ^ shr(x, 3);
  }

  function gamma1(x) {
    return rotr(x, 17) ^ rotr(x, 19) ^ shr(x, 10);
  }


  str = utf8_encode(str);
  strlen = str.length*charsize;
  str = str2binb(str);

  str[strlen >> 5] |= 0x80 << (24 - strlen % 32);
  str[((strlen + 64 >> 9) << 4) + 15] = strlen;

  for (var i = 0; i < strlen; i += 16) {
    a = H[0];
    b = H[1];
    c = H[2];
    d = H[3];
    e = H[4];
    f = H[5];
    g = H[6];
    h = H[7];

    for (var j = 0; j < 64; j++) {
      if (j < 16) {
        W[j] = str[j + i];
      } else {
        W[j] = safe_add_2(safe_add_2(safe_add_2(gamma1(W[j - 2]), W[j - 7]), gamma0(W[j - 15])), W[j - 16]);
      }

      T1 = safe_add_2(safe_add_2(safe_add_2(safe_add_2(h, sigma1(e)), ch(e, f, g)), K[j]), W[j]);
      T2 = safe_add_2(sigma0(a), maj(a, b, c));

      h = g;
      g = f;
      f = e;
      e = safe_add_2(d, T1);
      d = c;
      c = b;
      b = a;
      a = safe_add_2(T1, T2);
    }

    H[0] = safe_add_2(a, H[0]);
    H[1] = safe_add_2(b, H[1]);
    H[2] = safe_add_2(c, H[2]);
    H[3] = safe_add_2(d, H[3]);
    H[4] = safe_add_2(e, H[4]);
    H[5] = safe_add_2(f, H[5]);
    H[6] = safe_add_2(g, H[6]);
    H[7] = safe_add_2(h, H[7]);
  }

  return binb2hex(H);
}
