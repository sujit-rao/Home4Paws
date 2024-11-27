document.addEventListener('DOMContentLoaded', function () {
    // Mobile Navigation Toggle
    const navToggle = document.getElementById('navToggle');
    const navLinks = document.getElementById('navLinks');

    navToggle.addEventListener('click', () => {
        navLinks.classList.toggle('active');
    });

    // Image Slider Functionality
    let slideIndex = 0;
    const slides = document.querySelectorAll('.slide');
    const dots = document.querySelectorAll('.dot');

    function showSlides() {
        // Hide all slides
        slides.forEach(slide => {
            slide.style.opacity = 0;
            slide.style.display = "none";
        });

        // Remove active class from all dots
        dots.forEach(dot => {
            dot.classList.remove('active');
        });

        // Show current slide
        slideIndex++;
        if (slideIndex > slides.length) {
            slideIndex = 1;
        }

        slides[slideIndex - 1].style.display = "block";
        setTimeout(() => {
            slides[slideIndex - 1].style.opacity = 1;
        }, 10);
        dots[slideIndex - 1].classList.add('active');

        // Change slide every 5 seconds
        setTimeout(showSlides, 5000);
    }

    // Initialize slider
    showSlides();

    // Manual slide navigation
    window.currentSlide = function (n) {
        slideIndex = n;
        slides.forEach(slide => {
            slide.style.opacity = 0;
            slide.style.display = "none";
        });
        dots.forEach(dot => {
            dot.classList.remove('active');
        });
    }
});

// Fetching the Geolocation of the user

const API_KEY = "eb45feb6ff814cce95b55838232412"
const BASE_URL = "http://api.weatherapi.com/v1"
if ("geolocation" in navigator) {
    navigator.geolocation.getCurrentPosition(
        async (position) => {
            const { latitude, longitude } = position.coords;


            console.log(`Latitude: ${latitude}, Longitude: ${longitude}`);

            const response = await fetch(`http://api.weatherapi.com/v1/search.json?key=${API_KEY}&q=${latitude},${longitude}`)
            const data = await response.json()
            var city = data[0].name;
            city=city.toLowerCase();
            const state = data[0].region;
            console.log(city);

            const links = document.querySelectorAll(".findapet_href");
            links.forEach(link => {
            link.href = `/findapet/${city}`;
            });

        },
        (error) => {
            console.error("Error fetching location:", error.message);
            alert("Kindly Trun ON your Location.");
        }
    );
} else {
    console.error("Geolocation is not supported by this browser.");
}


// SignIN form
// const signinForm = document.getElementById('sign.inForm');
// if (signinForm) {
//     signinForm.addEventListener('submit', function (e) {
//         e.preventDefault();

//         const formData = {
//             email: e.target.email.value,
//             password: e.target.password.value,
//         };

//         const validateEmail = (email) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);

//         const validatePassword = (password) => password.length === 8 && password === '12345678';

//         if (!validateEmail(formData.email) || !validatePassword(formData.password)) {
//             alert('Invalid email or password');
//             return;
//         }

//         // Redirect to landing page
//         window.location.href = "../Landing/Landing.html";
//         e.target.reset();
//     });
// }

// SignUP form
// const signupForm = document.getElementById('signupForm');
// if (signupForm) {
//     signupForm.addEventListener('submit', async function (e) {
//         e.preventDefault();

//         const formData = {
//             name: e.target.name.value,
//             email: e.target.email.value,
//             password: e.target.password.value,
//             phoneNumber: e.target.phoneNumber.value,
//             city: e.target.city.value,
//             country: e.target.country.value,
//         };

//         const validateEmail = (email) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);

//         const validatePassword = (password) => password.length >= 8;

//         if (!validateEmail(formData.email)) {
//             alert('Please enter a valid email address.');
//             return;
//         }

//         if (!validatePassword(formData.password)) {
//             alert('Password must be at least 8 characters long.');
//             return;
//         }

//         alert('Signup successful! Welcome to Pet Companion.');
//         // Redirect to sign-in page
//         window.location.href = "../Signin/Signin.html";
//         e.target.reset();
//     });
// }


// PEt data upload form


const imageInput = document.getElementById('petImage');
const imagePreview = document.getElementById('imagePreview');
const fileNameDisplay = document.getElementById('fileName');
const imageUploadArea = document.querySelector('.image-upload-area');

imageInput.addEventListener('change', function (event) {
    const file = event.target.files[0];

    if (file) {
        // Update file name
        fileNameDisplay.textContent = file.name;

        // Create image preview
        const reader = new FileReader();

        reader.onload = function (e) {
            imagePreview.src = e.target.result;
            imagePreview.style.display = 'block';
            imageUploadArea.querySelector('span').style.display = 'none';
        }

        reader.readAsDataURL(file);
    } else {
        // Reset if no file selected
        fileNameDisplay.textContent = 'No file selected';
        imagePreview.style.display = 'none';
        imageUploadArea.querySelector('span').style.display = 'block';
    }
});




// Form submission
// const petUploadForm = document.getElementById('petUploadForm');
// if (petUploadForm) {
//     petUploadForm.addEventListener('submit', function (e) {
//         e.preventDefault();
//         alert('Form submitted!');

//         // Collect form data
//         const formData = new FormData(e.target);

//         // Log form data
//         for (let [key, value] of formData.entries()) {
//             console.log(`${key}: ${value}`);
//         }
//     });
// }




/*----------------------------DELETE POST-------------------------*/
function post_delete_btn_clicked(id) {
    Swal.fire({
        title: "Are you sure?",
        text: "You want to delete this post permanently?",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        confirmButtonText: "Yes, delete it!"
    }).then((result) => {
        if (result.isConfirmed) {
            setTimeout(function () {
                window.location.href = `deletepost/${id}`;
            }, 500);
        }
    });
}
/*----------------------------------------------------------------------*/
/*-----------------EDIT SELECTION option (Edit-Post Page)------------------*/
function select_edit_selection_opt(petgender) {
    // alert(college)
    // alert(pgfor)
    document.getElementById("petGender").value = petgender;
}


/*----------------------------------------------------------------------*/


// ---------------------------Removing Message Div-------------------------
function remove_message_div(){
    document.getElementById("message_div").style.display="none";
}
// -----------------------------------------------------------