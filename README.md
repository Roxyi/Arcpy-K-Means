# Arcpy-K-Means
Implement k-means clustering algorithm in ArcGIS

There are quite limited machine learning algorithms in ArcGIS pro but not in basic ArcGIS. To fill the gap, I came up with the idea that making some ArcTools based on Python scripts that introduce data mining into ArcGIS.

The idea is quite simple. Using Arcpy to get the values in the attribute table and storing them into arrays, then you can use these arrays as the input to k-means clustering algorithm.

I referred to other's code for k-means clustering algorithm. Sorry for the original author of that piece of code because I cannot remember whom I referred to. 

My code was intended for k-means in two-dimensional space. You can apply it to higher dimension by reading more attribute fields. Since the k-means part is separated from the the part of reading the values in the attribute table, you can also implement other machine learning algorithm like DBSCAN, KNN. 
