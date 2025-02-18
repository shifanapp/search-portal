    document.addEventListener("DOMContentLoaded", function () {
      function showSection(sectionId, pushState = true) {
        // Hide all sections
        document.querySelectorAll(".content-section").forEach(section => {
          section.classList.remove("active");
        });
    
        // Show the selected section
        const targetSection = document.getElementById(sectionId);
        if (targetSection) {
          targetSection.classList.add("active");
    
          // Construct new URL
          let newUrl = sectionId === "dashboard" 
            ? "/experts/dashboard" 
            : `/experts/${sectionId}`;
    
          // Update URL without reloading (only if manually clicked)
          if (pushState) {
            history.pushState({ section: sectionId }, "", newUrl);
          }
        }
      }
    
      // Load section from URL on page load
      const path = window.location.pathname.split("/").filter(Boolean);
      const section = path.length > 2 ? path[2] : "dashboard"; // Extract section from URL
      showSection(section, false); // Don't push state on initial load
    
      // Handle browser Back/Forward button (Prevents page refresh)
      window.addEventListener("popstate", function (event) {
        if (event.state && event.state.section) {
          showSection(event.state.section, false); // Don't push state when going back
        }
      });
    
      // Attach click event to sidebar links
      document.querySelectorAll(".sidebar a").forEach(link => {
        link.addEventListener("click", function (event) {
          event.preventDefault();
          const sectionId = this.getAttribute("onclick").match(/'([^']+)'/)[1];
          showSection(sectionId);
        });
      });
    });
    
    function showSection(sectionId) {
      document.querySelectorAll('.content-section').forEach(section => {
        section.style.display = 'none';
      });
      document.getElementById(sectionId).style.display = 'block';

      document.querySelectorAll('.sidebar a').forEach(link => {
        link.classList.remove('active');
      });
      document.querySelector(`[onclick="showSection('${sectionId}')"]`).classList.add('active');

      // Close sidebar after clicking (for mobile)
      if (window.innerWidth < 768) {
        document.querySelector('.sidebar').classList.remove('active');
      }
    }

    function toggleSidebar() {
      document.querySelector('.sidebar').classList.toggle('active');
    }
  // Function to show toast
  function showLogoutToast() {
      var toastEl = document.getElementById("logoutToast");
      var toast = new bootstrap.Toast(toastEl);
      toast.show();
  }

  // Check if logout was triggered using a cookie
  window.onload = function () {
      if (document.cookie.includes("logout_success=true")) {
          showLogoutToast(); 
          document.cookie = "logout_success=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
      }
  };
