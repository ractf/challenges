# Writeup

So this one is rather straightforward, you unzip the video and look at the exif data. It has an author of "muziyongshixin" and a description of "https://dl.acm.org/doi/abs/10.1145/3323873.3325011" which links to the research paper in question. Then you extract the cover art image which is the cover file for the steg'd image. It's not immediately obvious by looking and no amount of trivial statistical analysis tools will find anything meaningful.

However, you do not need to go that far to read the research paper, you just google the name and the second result is https://github.com/muziyongshixin/pytorch-Deep-Steganography which is precisely what we need. The code has few depdencies, so go ahead and install those, fortunately tensorflow and its 1 million depdendencies aren't requred, neither is a GPU. Just clone repo, install deps from requirements.txt (remove shutil why is that even there).

The code obviously won't work out of the box, **see the main.patch in Hints** for the overall idea but it largely comes down to applying workarounds to make it work for CPU and tweaking it so it takes in our cover image:

```diff
-        Hnet.load_state_dict(torch.load(opt.Hnet))
+        Hnet.apply(weights_init)
+        Hnet.load_state_dict(torch.load(opt.Hnet, map_location=torch.device('cpu')))
```

Then we need to set our imageSize values globally, the default is 256x256, this won't work, so just look at the dimensions of the cover art. Go ahead and set them throughout the program, it's height x width btw (btw I use arch):

```diff

+imsg_1 = 1024
+imsg_2 = 2048

-transforms.Resize([opt.imageSize, opt.imageSize]),
+transforms.Resize([imsg_1, imsg_2]),

```

Lastly, change the Reveal network to use the Cover file and save it individually. Delete all the exising images under the `example_code` test directory, place the cover file there and copy it with a different name (this is a workaround you can also modify the code to make it work with just one file, but that's up to you, both are equally valid solutions)

```diff
+rev_secret_img = Rnet(Variable(cover_img))
+with torch.no_grad():
+    secret_imgv = Variable(secret_img)

+vutils.save_image(containerFrames, f"{save_path}/thumb.png")
+vutils.save_image(revSecFrames, f"{save_path}/revsec_thumb.png")

```

> See the full patch under Hints for detailed info, most of it is just find and replace work that any participant should be able to do.

Then run the program and watch it spit out the secret image containing the flag, it may take up to half an hour depending on what CPU you have. I've tested this on a 2007 Xeon E5320 @ 1.86GHz (yes my £9.50 meme server) and it's taken me 23 minutes to extract it. Enough time for a few coffees.

# Flag

`ractf{n3ur4l_n3tw0rks_ftw!}`