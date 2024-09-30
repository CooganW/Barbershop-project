'use strict';

// Base URL for API calls
const BASE_URL = 'http://localhost:8000/api/';


// Add event on element
const addEventOnElem = function (elem, type, callback) {
  if (elem.length > 1) {
    for (let i = 0; i < elem.length; i++) {
      elem[i].addEventListener(type, callback);
    }
  } else {
    elem.addEventListener(type, callback);
  }
}


// Navbar toggle
const navbar = document.querySelector("[data-navbar]");
const navToggler = document.querySelector("[data-nav-toggler]");
const navLinks = document.querySelectorAll("[data-nav-link]");

const toggleNavbar = () => navbar.classList.toggle("active");
addEventOnElem(navToggler, "click", toggleNavbar);

const closeNavbar = () => navbar.classList.remove("active");
addEventOnElem(navLinks, "click", closeNavbar);


// Header & back top btn active when scroll down to 100px
const header = document.querySelector("[data-header]");
const backTopBtn = document.querySelector("[data-back-top-btn]");

const headerActive = function () {
  if (window.scrollY > 100) {
    header.classList.add("active");
    backTopBtn.classList.add("active");
  } else {
    header.classList.remove("active");
    backTopBtn.classList.remove("active");
  }
}

addEventOnElem(window, "scroll", headerActive);


// Filter function
const filterBtns = document.querySelectorAll("[data-filter-btn]");
const filterItems = document.querySelectorAll("[data-filter]");

let lastClickedFilterBtn = filterBtns[0];

const filter = function () {
  lastClickedFilterBtn.classList.remove("active");
  this.classList.add("active");
  lastClickedFilterBtn = this;

  for (let i = 0; i < filterItems.length; i++) {
    if (this.dataset.filterBtn === filterItems[i].dataset.filter ||
      this.dataset.filterBtn === "all") {
      filterItems[i].style.display = "block";
      filterItems[i].classList.add("active");
    } else {
      filterItems[i].style.display = "none";
      filterItems[i].classList.remove("active");
    }
  }
}

addEventOnElem(filterBtns, "click", filter);


// Barber Authentication
const authForm = document.getElementById('auth-form');
if (authForm) {
  authForm.addEventListener('submit', async function (e) {
    e.preventDefault();

    const username = document.getElementById('username').value.trim();
    const password = document.getElementById('password').value.trim();

    // Basic validation
    if (!username || !password) {
      alert("Username and password are required.");
      return;
    }

    try {
      const response = await fetch(`${BASE_URL}barbers/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }),
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Authentication failed');
      }

      const result = await response.json();
      console.log('Authentication response:', result);

      // Store the token in localStorage
      const token = result.token;
      localStorage.setItem('authToken', token);  // Store token

      window.location.href = '/time-slot-manager/'; // Redirect on success

    } catch (error) {
      console.error('Error:', error);
      alert(error.message || 'Error occurred during authentication');
    }
  });
}


// Time Slot Management
const timeSlotForm = document.getElementById('time-slot-form');
if (timeSlotForm) {
  timeSlotForm.addEventListener('submit', async function (e) {
    e.preventDefault();
    const startTime = document.getElementById('start-time').value;
    const endTime = document.getElementById('end-time').value;

    // To check if end time is later than start time
    if (new Date(endTime) <= new Date(startTime)) {
      document.getElementById('error-message').textContent = 'End time must be later than start time.';
      document.getElementById('error-message').style.display = 'block';
      return;
    }

    // Proceed with API call to add time slot
    try {
      const response = await fetch(`${BASE_URL}time-slots/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ start_time: startTime, end_time: endTime }),
      });

      if (!response.ok) {
        const errorMessage = await response.json();
        console.error(errorMessage);
        throw new Error('Failed to add time slot');
      }

      const result = await response.json();
      console.log('Time slot added:', result);
      fetchTimeSlots();

    } catch (error) {
      console.error('Error:', error);
      document.getElementById('error-message').textContent = error.message || 'Error occurred while adding the time slot';
      document.getElementById('error-message').style.display = 'block';
    }
  });
}


// Fetch and display time slots
async function fetchTimeSlots() {
  try {
    const token = localStorage.getItem('authToken');
    const response = await fetch(`${BASE_URL}time-slots/`, {
      method: 'GET',
      headers: {
        'Authorization': `Token ${token}`,
        'Content-Type': 'application/json'
      }
    });

    console.log('Full response:', response);

    const contentType = response.headers.get('content-type');
    if (!contentType || !contentType.includes('application/json')) {
      const textResponse = await response.text();
      console.error('Non-JSON response:', textResponse);
      throw new Error('Expected JSON, but got something else (possibly an error page).');
    }

    if (!response.ok) {
      const errorMessage = await response.json();
      console.error('Error message from server:', errorMessage);
      throw new Error('Failed to fetch time slots');
    }

    const timeSlots = await response.json();
    const timeSlotList = document.getElementById('time-slot-list');

    if (timeSlotList) {
      timeSlotList.innerHTML = '';

      if (timeSlots.length === 0) {
        timeSlotList.innerHTML = '<li>No available time slots</li>';
      } else {
        timeSlots.forEach(slot => {
          const listItem = document.createElement('li');
          listItem.textContent = `${slot.start_time} - ${slot.end_time}`;
          timeSlotList.appendChild(listItem);
        });
      }
    }
  } catch (error) {
    console.error('Error fetching time slots:', error);
    alert(error.message || 'An error occurred while fetching time slots');
  }
}


// Fetch time slots on page load
if (document.getElementById('time-slot-list')) {
  fetchTimeSlots();
}