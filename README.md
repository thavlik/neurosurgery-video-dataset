![](./images/output.gif)
# Neurosurgery Video Dataset
[<img src="https://img.shields.io/badge/maintenance%20status-actively%20developed-brightgreen">](https://github.com/thavlik/neurosurgery-video-dataset)
[<img src="https://img.shields.io/badge/License-Apache_2.0-orange.svg">](./LICENSE-Apache)
[<img src="https://img.shields.io/badge/License-MIT-lightblue.svg">](./LICENSE-MIT)
[<img src="https://img.shields.io/badge/Language-python-FFD43B.svg">](https://www.python.org/)

This is a compilation of YouTube videos that has been processed for use in a machine learning dataset. The goal is to facilitate the creation of tools that provide per-pixel labels for features ranging from the surgeon's tools to the patient's tissues. I think such tools have the potential to greatly enhance the value of surgical e-Shadowing, giving students the ability to click parts of the video itself to get more information about the anatomy.

## TODO
- label more frames
- overfit model on toy dataset
- create a frame-filter model using [t4vd](https://github.com/thavlik/t4vd)
- train a variational auto-encoder on the t4vd-filtered frames
- determine if the VAE improves data efficiency
- evaluate amazon mturk with this project's data

## License
### Data
Video data is property of the respective authors:
- [Dr. Farhad Limonadi (MicroNeuroSurgeryOrg)](https://www.youtube.com/@MicroNeuroSurgeryOrg/)

### Code
All code in this repository is released under [MIT](LICENSE-MIT) / [Apache 2.0](LICENSE-Apache) dual license, which is extremely permissive. Please open an issue if somehow these terms are insufficient.
