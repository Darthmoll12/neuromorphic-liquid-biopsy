# neuromorphic-liquid-biopsy
Nathaniel Moll

Biochemistry and Molecular Biology Major, Honors Scholar, Liberty University
March 24th, 2026

Undergraduate Thesis

Committee Chair: Dr. Gary Isaacs, Department of Biology and Chemistry
Committee Member: Dr. Gregory Raner, Department of Biology and Chemistry


### Overview

This project will investigate the use of Spiking Neural Networks (SNNs) for real-time cancer detection from circulating cell-free DNA (cfDNA) nanopore sequence data. By implementing multi-channel SNN architecture, cfDNA features will be characterized, including fragment length and end motifs. Each feature will be used to generate a response from the SNN system: Cancer detection or no cancer detection. The models will be built in a hardware-aware simulation allowing for training and validation. Metrics such as accuracy and energy efficiency will be analyzed and compared to traditional machine learning models. This method will demonstrate a novel application of SNNs for genetic analysis and cancer detection, enabling the use of point-of-care liquid biopsy devices.

### Background Information/Motivation
Modern precision oncology requires real-time monitoring of tumor status and adaptation to inform treatment strategies that rely on time-sensitive molecular information. The ability to rapidly gain insight into disease condition or progression can therefore improve clinical outcomes for cancer patients. Liquid biopsy is one recent development that seeks to support this initiative. Current methods utilize next generation sequencing to analyze circulating tumor DNA from blood samples. While features like mutations and methylation patterns can be characterized, the process requires time-consuming sample preparations and heavy, centralized computing infrastructure for base calling and sequence alignment. This can delay results by up to 1 – 2 weeks, which can have negative clinical consequences since cancer is a dynamic disease that adapts rapidly at molecular timescales. One liquid biopsy experiment was reported to yield results in 6 – 8 hours from blood draw, however it was reported that the GPU-based computational analysis consumed approximately 300 watts and required specialized architecture that limited useful deployment. Therefore, there are substantial bottlenecks in current liquid biopsy methods: Computational efficiency and ease of deployment. Removing these bottlenecks may enable point-of-care liquid biopsy capabilities that can give rapid results in a matter of minutes. However, for such a technology to exist, computational complexities must be reduced to where the necessary algorithms can be completed on-chip, that is, entirely within the point-of-care device. 

To address limitations in portability and processing time, recent advances in the field include the development of portable and hand-held nanopore sequencing devices to analyze cell free DNA (cfDNA) fragments in the bloodstream. Oftentimes, fragment features can inform whether DNA fragments came from healthy or cancerous tissues, making fragment analysis a useful method in cancer biomarker detection. Nanopore devices like the Oxford Nanopore Technologies MinION provide for a real-time and portable platform for such fragment sequencing. However, the computational cost associated with analyzing nanopore data with traditional machine learning (ML) is expensive. Thus, these algorithms do not lend themselves towards use for edge deployment and therefore rapid results. Proposed herein is a novel method to reduce the computational cost of liquid biopsy analysis to such a degree that enables on-chip processing and results within minutes, faster than even the best GPU-based systems and with simpler deployment.

Using an emerging computational paradigm called neuromorphic computing (which utilizes algorithms called Spiking Neural Networks or SNNs), such a liquid biopsy architecture can be implemented. Neuromorphic computing is a type of artificial intelligence computing that mimics the brain in its structure, allowing for event-based computation that enables extreme energy efficiency compared to traditional ML algorithms. Since DNA nanopore data is temporal and event-driven data, SNNs are ideal algorithms for cfDNA fragment signal processing.

Therefore, it is the objective of this research to implement and train SNNs on cfDNA nanopore data to extract features and identify cancer-related biomarkers in a physiologically relevant manner. If successful, this study will demonstrate a novel application of neuromorphic computing to analyze cfDNA data for the purposes of cancer detection, while achieving a dramatic lowering of computational energy cost associated with the process.

### Research Questions

The research seeks to answer the following questions: 
1.	Feasibility: Can SNNs extract multi-modal features (fragment length, end motifs, etc.) from cfDNA nanopore data to achieve reliable cancer detection after model validation?
2.	Performance: Does SNN architecture achieve greater than or comparable accuracy, sensitivity, and specificity to traditional GPU-based systems while maintaining significantly improved energy efficiency?

### Repository Structure

neuromorphic-liquid-biopsy/
- data/                       # Data directories (not tracked)
- simulation/                  # Reference sequence design and Squigulator pipeline
- encoding/                    # Spike train encoding scripts from nanopore squiggles
- models/                      # SNN channel architectures (Lava framework)
- training/                    # Training scripts per channel
- evaluation/                  # Benchmarking, energy profiling, precision/recall, and other metrics
- notebooks/                   # Exploratory and validation notebooks
- docs/                        # Methods documentation


### Expected Outcomes and Significance

The expected outcomes of this research should demonstrate how neuromorphic computation provides increased energy efficiency by orders of magnitude that may enable on-chip function. In addition, results should match or exceed published assays which are reported to achieve ≥90% sensitivity and ≥95% specificity in detecting circulating tumor DNA fragments using traditional methods, while also consuming significantly less power. For this to be possible, it must also be demonstrated that SNNs can extract clinically relevant features from nanopore data. If successful, the research would be one of the first demonstrations of neuromorphic computing for genomic analysis and cancer detection, given that the models are benchmarked and validated adequately. This would immediately create new applications in the development of point-of-care liquid biopsy devices leading to rapid diagnostic results. If the bottlenecks of current liquid biopsy methods are significantly reduced or removed, the only rate-limiting factor would be the isolation of the cfDNA fragments themselves.

### Limitations and Scope

This thesis aims to demonstrate a proof-of-concept of the technical feasibility of using SNNs to detect circulating tumor DNA as found in the bloodstream. The models will be validated using public cancer and cell line data and performance will be analyzed and compared to current traditional approaches. The thesis does not aim to produce wet lab validation on real samples or sequencing hardware, and the process will be a hardware simulation using software designed by Intel for this purpose. In addition, the project will not demonstrate an end-to-end system, but rather only the computational analysis segment of a liquid biopsy system. This is an appropriate scope since computational validation is enough to indicate feasibility and public data sets provide for sufficient validation that can prepare for wet lab experiments. Since neuromorphic hardware is challenging to acquire, hardware simulations offer a realistic and systemic analysis without having to obtain real chips or be limited by certain hardware functionalities.