function drawImage(img) {
  const canvas = document.getElementById("img"),
    context = canvas.getContext("2d");

  image = new Image();
  image.src = img;
  image.onload = function () {
    const canvasWidth = canvas.parentElement.clientWidth;
    const canvasHeight =
      canvas.parentElement.clientWidth *
      (image.naturalHeight / image.naturalWidth);
    canvas.width = canvasWidth;
    canvas.height = canvasHeight;

    var scale = Math.min(
      canvasWidth / image.width,
      canvasHeight / image.height
    );
    const x = canvasWidth / 2 - (image.width / 2) * scale;
    const y = canvasHeight / 2 - (image.height / 2) * scale;
    context.drawImage(image, x, y, image.width * scale, image.height * scale);
  };
}

async function detectFaces(file) {
  const fileReader = new FileReader();

  fileReader.onload = (e) => {
    drawImage(e.target.result);
  };

  fileReader.readAsDataURL(file);

  this.value = null;

  const url = "http://0.0.0.0:5000//api/v1/";

  const res = await fetch(url, {
    method: "POST",
    mode: "cors",
    cache: "no-cache",
    credentials: "same-origin",
    referrerPolicy: "no-referrer",
    body: file,
  });

  const reader = await res.body.getReader();

  const stream = new ReadableStream({
    start(controller) {
      return pump();

      function pump() {
        return reader.read().then(({ done, value }) => {
          // When no more data needs to be consumed, close the stream
          if (done) {
            controller.close();
            return;
          }

          // Enqueue the next data chunk into our target stream
          controller.enqueue(value);
          return pump();
        });
      }
    },
  });

  const response = new Response(stream);

  const blob = await response.blob();

  const base64Reader = await new FileReader();
  base64Reader.readAsDataURL(blob);
  base64Reader.onloadend = function () {
    const base64data = base64Reader.result;
    drawImage(base64data);
  };
}

function handleBrowse() {
  detectFaces(this.files[0]);
}

document
  .querySelector("#input")
  .addEventListener("change", handleBrowse, false);

function preventDefaults(e) {
  e.preventDefault();
  e.stopPropagation();
}

function handleDrop(e) {
  let dt = e.dataTransfer;
  let files = dt.files;

  detectFaces(files[0]);
}

const dropArea = document.getElementById("drop-area");

["dragenter", "dragover", "dragleave", "drop"].forEach((eventName) => {
  dropArea.addEventListener(eventName, preventDefaults, false);
});

dropArea.addEventListener("drop", handleDrop, false);
