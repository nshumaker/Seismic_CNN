## Access and Use
Completed notebook saved in "notebooks" folder. To reproduce the workflow, clone the repo and run the environment.yml file to download and install the required packages. The repo sturcture was access from Rafael Pinto's cookie-cutter repo.
Helper functions used in the notebook are saved in the src/utils.py folder.

# Motivation
While seismic processing is heavy on computation and quantification, the discipline of seismic interpretation is highly descriptive and often performed by stratigraphers who have deep expertise in recognizing rock fabrics, textures, and depositional relationships through examination of outcrops and thin sections. Seismic stratigraphy is similarly descriptive; facies are “hummocky”, “continuous”, “mottled”, “striped”, “truncated”, “attenuated”, etc. and when viewed through a sequence stratigraphy lens: “clinoforms”, “transgressive”, “regressive”, “high-stand tract”, or a geophysical lens: “attenuated”, “bright”, “noise trains”, “over-migrated”, etc. 

# Analysis (See notebooks folder)

# Discussion
Traditional quantitative efforts of the past have been focused around structural imaging, noise attenuation and seismic attribute calculation. However, borrowing from techniques developed in the computer vision field, deep neural networks when applied to seismic images may be a new source of valuable interpretive innovation. To further explain, neural networks are comprised of many layers of filters that decompose input arrays of images into hundreds of unique features of varying scales across the input images. These filter layers typically encode gross scale features shallow in the network and progressively smaller, more abstract features deeper in the network. Each image is encoded as a unique combination of filter activations when forward propagated through the network. 

While even a novice interpreter would be able to compare and contrast the two seismic images in Figure 1, the neural network has quantitatively encoded more features at all scales, further setting the stage for statistical analysis and input into machine learning algorithms. While an interpreter is always needed to determine what an image means, the neural network provides additional, less biased tools to identify key features, quantify seismic characteristics, and ultimately de-risk prospect inventories and help safely plan and drill wells. "# Seismic_CNN.git" 
