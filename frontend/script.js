const API_URL = "http://127.0.0.1:8000/predict"; // FastAPI endpoint
const CONFIDENCE_THRESHOLD = 80;

let cart = [];

document.getElementById("recognize-btn").addEventListener("click", recognizeItems);
document.getElementById("checkout-btn").addEventListener("click", checkout);

async function recognizeItems() {
    const fileInput = document.getElementById("image-upload");
    if (!fileInput.files[0]) {
        alert("Please select an image first.");
        return;
    }

    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

    const response = await fetch("http://127.0.0.1:8000/predict", {
        method: "POST",
        body: formData
    });

    const result = await response.json();
    console.log("BACKEND RESPONSE:", result);   // 🔥 IMPORTANT

    displayRecognizedItems([result]);
}


function displayRecognizedItems(items) {
    const list = document.getElementById("recognized-items");
    list.innerHTML = "";

    items.forEach(item => {
        const lowConfidence = item.confidence < CONFIDENCE_THRESHOLD;

        const li = document.createElement("li");
        li.className = lowConfidence ? "low-confidence" : "";



        let buttonsHTML = `
            <button onclick="addToCart('${item.class}', ${item.price})">
                Add to Cart
            </button>
        `;

        if (lowConfidence) {
            buttonsHTML += `
                <button onclick="retryPrediction()">
                    Retry Image
                </button>
                <button onclick="manualEntry()">
                    Manual Type
                </button>
            `;
        }

        li.innerHTML = `
            <span>
              <strong>${item.class}</strong><br>
              Confidence: ${item.confidence}% 
              ${lowConfidence ? "<span style='color:red;'>(Low confidence)</span>" : ""}
              <br>
              Price: ₹${item.price}
            </span>
            <div style="display:flex; gap:10px; margin-top:10px;">
                ${buttonsHTML}
            </div>
        `;

        list.appendChild(li);
    });
}



function addToCart(name, price) {
    cart.push({ name, price });
    updateCartDisplay();
}

function retryPrediction() {
    document.getElementById("image-upload").value = "";
    alert("Please upload a clearer image and try again.");
}

function manualEntry() {
    const itemName = prompt("Enter item name manually:");
    if (!itemName) return;

    const price = prompt("Enter price for " + itemName + ":");
    if (!price || isNaN(price)) {
        alert("Invalid price");
        return;
    }

    addToCart(itemName, parseFloat(price));
}


function updateCartDisplay() {
    const list = document.getElementById("cart-items");
    list.innerHTML = "";

    let total = 0;

    cart.forEach((item, index) => {
        total += item.price;
        const li = document.createElement("li");
        li.innerHTML = `
            <span>${item.name} - ₹${item.price}</span>
            <button onclick="removeFromCart(${index})">Remove</button>
        `;
        list.appendChild(li);
    });

    document.getElementById("total-price").textContent = total.toFixed(2);
}

function removeFromCart(index) {
    cart.splice(index, 1);
    updateCartDisplay();
}

function checkout() {
    if (cart.length === 0) {
        alert("Your cart is empty!");
        return;
    }

    alert(`Checkout successful! Total: ₹${document.getElementById("total-price").textContent}`);
    cart = [];
    updateCartDisplay();
}

const video = document.getElementById("video");
const canvas = document.getElementById("canvas");
const captureBtn = document.getElementById("capture-btn");

// Start camera
navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => {
        video.srcObject = stream;
    })
    .catch(err => {
        alert("Camera access denied");
        console.error(err);
    });

// Capture frame & send to backend
captureBtn.addEventListener("click", async () => {
    const context = canvas.getContext("2d");
    context.drawImage(video, 0, 0, canvas.width, canvas.height);

    canvas.toBlob(async (blob) => {
        const formData = new FormData();
        formData.append("file", blob, "camera.jpg");

        try {
            const response = await fetch("http://127.0.0.1:8000/predict", {
                method: "POST",
                body: formData
            });

            const result = await response.json();
            displayRecognizedItems([result]);

        } catch (error) {
            alert("Camera prediction failed");
            console.error(error);
        }
    }, "image/jpeg");
});
