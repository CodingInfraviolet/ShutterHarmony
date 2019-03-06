# ShutterHarmony

When taking photographs, I like to take multiple photograps of the same thing,
and then choose the sharpest image for later editing. However, I found that
this process takes far too much time, and it's often difficult to judge which
photograph is sharper when comparing to multiple others.

This project is meant to solve that problem. Given a directory, it searches
through all the ARW image files in that directory, groups similar images that
were taken within the same time frame, and sorts each group by sharpness. It then
emits a series of commands that creates a new directory for each group and copies
images into those directories, again sorted by sharpness.

Example usage:

```
➜  ShutterHarmony  git:(master) python ./src/main.py ./test/resources      
Loading images
Loaded ./test/resources/1C_blurry.ARW
Loaded ./test/resources/1A.ARW
Loaded ./test/resources/2A.ARW
Loaded ./test/resources/2G_blurry.ARW
Loaded ./test/resources/0B.ARW
Loaded ./test/resources/2F_blurry.ARW
Loaded ./test/resources/0C.ARW
Loaded ./test/resources/2D_blurry.ARW
Loaded ./test/resources/0D.ARW
Loaded ./test/resources/2B_blurry.ARW
Loaded ./test/resources/1E_blurry.ARW
Loaded ./test/resources/1B.ARW
Loaded ./test/resources/0A.ARW
Loaded ./test/resources/2E_blurry.ARW
Loaded ./test/resources/1D_blurry.ARW
Loaded ./test/resources/2C_blurry.ARW
mkdir -p ./test/resources/grouped
mkdir ./test/resources/grouped/0
cp ./test/resources/0D.ARW ./test/resources/grouped/0/0.ARW
cp ./test/resources/0A.ARW ./test/resources/grouped/0/1.ARW
cp ./test/resources/0C.ARW ./test/resources/grouped/0/2.ARW
cp ./test/resources/0B.ARW ./test/resources/grouped/0/3.ARW
mkdir ./test/resources/grouped/1
cp ./test/resources/1A.ARW ./test/resources/grouped/1/0.ARW
cp ./test/resources/1B.ARW ./test/resources/grouped/1/1.ARW
cp ./test/resources/1D_blurry.ARW ./test/resources/grouped/1/2.ARW
cp ./test/resources/1E_blurry.ARW ./test/resources/grouped/1/3.ARW
cp ./test/resources/1C_blurry.ARW ./test/resources/grouped/1/4.ARW
mkdir ./test/resources/grouped/2
cp ./test/resources/2A.ARW ./test/resources/grouped/2/0.ARW
cp ./test/resources/2B_blurry.ARW ./test/resources/grouped/2/1.ARW
cp ./test/resources/2G_blurry.ARW ./test/resources/grouped/2/2.ARW
cp ./test/resources/2C_blurry.ARW ./test/resources/grouped/2/3.ARW
cp ./test/resources/2E_blurry.ARW ./test/resources/grouped/2/4.ARW
cp ./test/resources/2D_blurry.ARW ./test/resources/grouped/2/5.ARW
cp ./test/resources/2F_blurry.ARW ./test/resources/grouped/2/6.ARW

```

# Roadmap

The following features may later be added:

* GUI for easier use
* Proper package manager / installer
* Faster loading by utilisting multiple threads / jpg preview
* Support for more file formats
* Loading images directly from a connected camera
