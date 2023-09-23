## Edge Eval Python
A python implementation of [edge eval](https://github.com/s9xie/hed_release-deprecated/tree/master/examples/eval).

The logic of the code is almost the same as that of the origin MATLAB implementation (see [References](#References)).
The core code is used directly  [edge-eval-python](https://github.com/Walstruzz/edge_eval_python).

I just added some optimizations for ease of use. Currently, BSDS, NYUD, BIPED, UDED can be used in one click, and other datasets can be easily eval by specifying GT.

## Requirements
* Python3
* Numpy
* Scipy >= 1.6.0
* g++
* Matplotlib

## Install
### 1. clone repository
``` shell
git clone https://github.com/Walstruzz/edge_eval_python.git
cd edge_eval_python
```

### 2. compile cxx library
Most of the code in this folder is copied from [davidstutz/extended-berkeley-segmentation-benchmark](https://github.com/davidstutz/extended-berkeley-segmentation-benchmark/tree/master/source).

Actually, there is a more efficient function in `Scipy` that can solve the CSA problem without compiling the following cxx codes...
``` shell
cd cxx/src
source build.sh
```

## Usage
### 1. save your results 

save your result like this: [https://github.com/Li-yachuan/CTFN-pytorch-master/blob/main/test.py](https://github.com/Li-yachuan/CTFN-pytorch-master/blob/main/test.py).

Make sure that there are two folders `mat` and `png` in the results folder to save the two forms of the prediction results

Let's say this folder is `/result`

Then the folder structure should be:  
``` 

\result  
....|-png  
....|...|-a.png  
....|...|-b.png  
....|....:  
....|-mat  
........|-a.mat    
........|-b.mat  
		:
```

### 2. Download GT
Download the project and unzip the GT in the folder `.\GT`. They are available [here](https://drive.google.com/drive/folders/1j1TU28PinKipOh0egf8tbzI7EetAbzKh?usp=sharing)




### 3.eval

####3.1  The simplest eval
just use  
``` shell
python eval.py [input dir] -d [dataset name]  -f
```

for example:

``` shell
python eval.py \result -d BSDS  -f
```

you can eval the result of BSDS500 in dir `\result` 

For higher automation, we implement automatic detection of folders with simple cycle. We use the `T` and `limit` parameters to control the sleep time and total wait time for the folder traversal, the default of which is 0.5 hours and 8 hours.

####3.2 No constant monitoring
If you only need to eval existing results, you can use `notwait` to cancel the automatic check and keep waiting, as follows:


``` shell
python eval.py \result -d BSDS -nw -f
```

####3.3 Default dataset

If you can include the dataset name in the path under eval, then you don't have to specify the dataset individually:


``` shell
python eval.py \result\bsds-result -nw -f
```

####3.4 multiple paths

You can specify multiple paths to eval multiple sets of results at the same time.You need to place multiple paths inside the "", separated by Spaces. There is no support for evaling multiple datasets at the same time, so multiple results should be on the same dataset.		

``` shell
python eval.py "\result\bsds-result \result\bsds-result2" -nw -f
```

####3.5 light version & full version

Evaluation of edge detection is known to be a very time-consuming process, in extreme cases even slower than training, such as on densely labeled datasets like BIPED.


To speed up eval, we divided eval into two versions, light and full, by controlling the sampling frequency of the threshold. The full version is currently the most commonly used thrs=99, and thrs=9 in light.

light version:
``` shell
python eval.py "\result\bsds-result \result\bsds-result2" -nw
```

full version:
``` shell
python eval.py "\result\bsds-result \result\bsds-result2" -nw -f
```

The light version is faster, but the accuracy will be about 0.5% lower than the full version, but the relative accuracy will not change, so we can use the light version to pick the best result, and then use the full version to get its true accuracy.

####3.6 show result

 
To see the results better, use the following command.

for full version:		

``` shell
python show.py "\result\bsds-result" -f
```

for light version:		

``` shell
python show.py "\result\bsds-result"
```

## Note
* The edges of the image are 1 and the background is 0. black background.


## Note (same as  [edge-eval-python](https://github.com/Walstruzz/edge_eval_python).)
* Because of the difference in calculation precision and the sensitivity of NMS threshold, the edge images may be **slightly** different.
* `match_edge_maps` samples points randomly (**so as Matlab**).
* Python and Matlab index files in different order, resulting in different order of `eval_bdry_img.txt`.
* Python version is slower than Matlab version. Should I implement more functions in `cxx/lib/solve_cas.so`?

## References
* [edge eval](https://github.com/s9xie/hed_release-deprecated/tree/master/examples/eval)
* [extended-berkeley-segmentation-benchmark](https://github.com/davidstutz/extended-berkeley-segmentation-benchmark).
* [bwmorph_thin](https://gist.github.com/joefutrelle/562f25bbcf20691217b8)
* [pdollar's image & video Matlab toolbox ](https://github.com/pdollar/toolbox)
* [pdollar's edge detection toolbox](https://github.com/pdollar/edges)
* [PyTorch Reimplementation of HED](https://github.com/xwjabc/hed)
* [edge-eval-python](https://github.com/Walstruzz/edge_eval_python).
