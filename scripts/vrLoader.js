
window.addEventListener('load', onVrViewLoad)
function onVrViewLoad() {
  var vrView = new VRView.Player('#image360', {
    video: 'bin/vrview/examples/video/congo_2048.mp4',
    is_stereo: true
  });
}