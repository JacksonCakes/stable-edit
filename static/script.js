const fileInput = document.querySelector(".file-input"),
canvas = document.querySelector("canvas"),
negPrompt = document.querySelector("textarea"),
prompt = document.querySelector(".prompt"),
toolBtns = document.querySelectorAll(".tool"),
filterOptions = document.querySelectorAll(".filter button"),
filterName = document.querySelector(".filter-info .name"),
stepValue = document.querySelector("#step-value"),
guideValue = document.querySelector("#guide-value"),
stepsSlider = document.querySelector("#steps-slider"),
guideSlider = document.querySelector("#guidance-slider"),
sizeSlider = document.querySelector("#size-slider"),
rotateOptions = document.querySelectorAll(".rotate button"),
previewImg = document.querySelector(".preview-img img"),
clearCanvas = document.querySelector(".clear-canvas"),
resetFilterBtn = document.querySelector(".reset-filter"),
chooseImgBtn = document.querySelector(".choose-img"),
saveImgBtn = document.querySelector(".save-img"),
generateBtn = document.querySelector(".center-con"),
ctx = canvas.getContext("2d",{ willReadFrequently: true });

let brightness = "100", saturation = "100", inversion = "0", grayscale = "0";
let rotate = 0, flipHorizontal = 1, flipVertical = 1;
// global variables with default value
let prevMouseX, prevMouseY, snapshot,
isDrawing = false,
selectedTool = "brush",
brushWidth = 50,
selectedColor = "#000";
let Undo = [];

let Redo = [];

const loadImage = () => {
    let file = fileInput.files[0];
    if(!file) return;
    previewImg.src = URL.createObjectURL(file);
    previewImg.addEventListener("load", () => {
        resetFilterBtn.click();
        document.querySelector(".container").classList.remove("disable");
        canvas.width = previewImg.clientWidth;
        canvas.height = previewImg.clientHeight;
    });
    
}
const startDraw = (e) => {
    isDrawing = true;
    prevMouseX = e.offsetX; // passing current mouseX position as prevMouseX value
    prevMouseY = e.offsetY; // passing current mouseY position as prevMouseY value
    ctx.beginPath(); // creating new path to draw
    ctx.lineJoin = 'round';
    ctx.lineCap = "round"
    ctx.lineWidth = brushWidth; // passing brushSize as line width
    ctx.strokeStyle = selectedColor; // passing selectedColor as stroke style
    ctx.fillStyle = selectedColor; // passing selectedColor as fill style
    // copying canvas data & passing as snapshot value.. this avoids dragging the image
    snapshot = ctx.getImageData(0, 0, canvas.width, canvas.height);
}

const drawing = (e) => {
    if(!isDrawing) return; // if isDrawing is false return from here
    ctx.putImageData(snapshot, 0, 0); // adding copied canvas data on to this canvas

    if(selectedTool === "brush" || selectedTool === "eraser") {
        if(selectedTool === "brush")
        {
            ctx.globalCompositeOperation="source-over";
        }
        else{
            ctx.globalCompositeOperation="destination-out";
        }
        // if selected tool is eraser then set strokeStyle to white 
        // to paint white color on to the existing canvas content else set the stroke color to selected color
        ctx.strokeStyle = selectedTool === "eraser" ? "#fff" : selectedColor;
        ctx.lineTo(e.offsetX, e.offsetY); // creating line according to the mouse pointer
        ctx.stroke(); // drawing/filling line with color
    } else if(selectedTool === "rectangle"){
        drawRect(e);
    } else if(selectedTool === "circle"){
        drawCircle(e);
    } else {
        drawTriangle(e);
    }
}
sizeSlider.addEventListener("change", () => brushWidth = sizeSlider.value); // passing slider value as brushSize
const applyFilter = () => {
    previewImg.style.transform = `rotate(${rotate}deg) scale(${flipHorizontal}, ${flipVertical})`;
    previewImg.style.filter = `brightness(${brightness}%) saturate(${saturation}%) invert(${inversion}%) grayscale(${grayscale}%)`;
}

toolBtns.forEach(btn => {
    btn.addEventListener("click", () => { // adding click event to all tool option
        // removing active class from the previous option and adding on current clicked option
        document.querySelector(".options-brush .active").classList.remove("active");
        btn.classList.add("active");
        selectedTool = btn.id;
    });
});

filterOptions.forEach(option => {
    option.addEventListener("click", () => {
        document.querySelector(".active").classList.remove("active");
        option.classList.add("active");
   

    });
});

const updateFilter = () => {
    stepValue.innerText = `${stepsSlider.value}`;
    
}
const updateGuide = () => {
    guideValue.innerText = `${guideSlider.value}`;
    
}

rotateOptions.forEach(option => {
    option.addEventListener("click", () => {
        if(option.id === "left") {
            let latest_edit = Undo[Undo.length - 1];
            // Erase top element
            // of the stack
            Undo.pop();
            previewImg.src = Undo[Undo.length - 1];
            // Push an element to
            // the top of stack
            Redo.push(latest_edit);
        } else if(option.id === "right") {
            // Stores the top element
            // of the stack
            let cur_edit = Redo[Redo.length - 1];
            // Erase the top element
            // of the stack
            previewImg.src = Redo.pop();
            // Push an element to
            // the top of the stack
            Undo.push(cur_edit);
        } else if(option.id === "horizontal") {
            flipHorizontal = flipHorizontal === 1 ? -1 : 1;
        } else {
            flipVertical = flipVertical === 1 ? -1 : 1;
        }
        //applyFilter();
    });
});

const resetFilter = () => {
    brightness = "100"; saturation = "100"; inversion = "0"; grayscale = "0";
    rotate = 0; flipHorizontal = 1; flipVertical = 1;
    filterOptions[0].click();
    applyFilter();
}

clearCanvas.addEventListener("click", () => {
    ctx.clearRect(0, 0, canvas.width, canvas.height); // clearing whole canvas
});

const saveImage = () => {
    const link = document.createElement("a"); // creating <a> element
    const img = document.createElement("img");
    const img_canvas = document.createElement("canvas");
    img_canvas.width = previewImg.clientWidth;
    img_canvas.height = previewImg.clientHeight;
    img_canvas.getContext("2d").drawImage(previewImg,0,0,img_canvas.width,img_canvas.height);
    link.href = img_canvas.toDataURL();  

    link.download = "image.jpg";
    link.click();
};

const sendData = () => {
    const link = document.createElement("a");
    const img = document.createElement("img");
    const img_canvas = document.createElement("canvas");
    img_canvas.width = previewImg.clientWidth;
    img_canvas.height = previewImg.clientHeight;
    img_canvas.getContext("2d").drawImage(previewImg,0,0,img_canvas.width,img_canvas.height);
    img.src = img_canvas.toDataURL();  

    link.download = "image.jpg";
    link.href = canvas.toDataURL();
    let formData = new FormData();
	formData.append('imageBase64' , img.src);
    formData.append('maskBase64' , link.href);
    formData.append("step",stepValue.innerText);
    formData.append("guidance",guideValue.innerText);
    formData.append('prompt' , prompt.value);
    formData.append("neg-prompt",negPrompt.value);
    $.ajax({
        type: "POST",
        url: "/imgEditing",
        data:formData,
        beforeSend:function(){
            previewImg.style.display = "none";
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            $(".dash-container").show();
        },
        processData: false,
        contentType: false,
        error: function(data){
            console.log("upload error" , data);
            console.log(data.getAllResponseHeaders());
        },
        success: function(data){
            $(".dash-container").hide();
            bytestring = data['image']
            const image_res = bytestring.split('\'')[1]
            previewImg.src = 'data:image/jpeg;base64,' + image_res;
            Undo.push(previewImg.src);
            previewImg.style.display = "block";

            console.log('success');
        }
      
      })
}

canvas.addEventListener("mousedown", startDraw);
canvas.addEventListener("mousemove", drawing);
canvas.addEventListener("mouseup", () => isDrawing = false);
stepsSlider.addEventListener("input", updateFilter);
guideSlider.addEventListener("input", updateGuide);
resetFilterBtn.addEventListener("click", resetFilter);
saveImgBtn.addEventListener("click", saveImage);
generateBtn.addEventListener("click", sendData);
fileInput.addEventListener("change", loadImage);
chooseImgBtn.addEventListener("click", () => fileInput.click());