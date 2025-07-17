

const menu = [
  {
    id: 1,
    title: "Leg Bracelet",
    category: "ORNAMENTS",
    price: 15.99,
    img: "./assets/img/beads4.webp",
    desc: `I'm baby woke mlkshk wolf bitters live-edge blue bottle, hammock freegan copper mug whatever cold-pressed `,
  },
  {
    id: 2,
    title: "Bailed Plastics",
    category: "BALES",
    price: 13.99,
    img: "./assets/img/production2.jpg",
    desc: `vaporware iPhone mumblecore selvage raw denim slow-carb leggings gochujang helvetica man braid jianbing. Marfa thundercats `,
  },
  {
    id: 3,
    title: "Bailed Plastics",
    category: "BALES",
    price: 6.99,
    img: "./assets/img/IMG-20221202-WA0007.webp",
    desc: `ombucha chillwave fanny pack 3 wolf moon street art photo booth before they sold out organic viral.`,
  },
  {
    id: 4,
    title: "Blue Pellets",
    category: "PELLETS",
    price: 20.99,
    img: "./assets/img/market.webp",
    desc: `Shabby chic keffiyeh neutra snackwave pork belly shoreditch. Prism austin mlkshk truffaut, `,
  },
  {
    id: 5,
    title: "Necklace",
    category: "ORNAMENTS",
    price: 22.99,
    img: "./assets/img/beads3.webp",
    desc: `franzen vegan pabst bicycle rights kickstarter pinterest meditation farm-to-table 90's pop-up `,
  },
  {
    id: 6,
    title: "Shreddered Flakes",
    category: "FLAKES",
    price: 18.99,
    img: "./assets/img/IMG-20221205-WA0006.jpg",
    desc: `Portland chicharrones ethical edison bulb, palo santo craft beer chia heirloom iPhone everyday`,
  },
  {
    id: 7,
    title: "Green PET Flakes",
    category: "FLAKES",
    price: 8.99,
    img: "./assets/img/production1.jpg",
    desc: `carry jianbing normcore freegan. Viral single-origin coffee live-edge, pork belly cloud bread iceland put a bird `,
  },
  {
    id: 8,
    title: "american classic",
    category: "3D-PRINT",
    price: 12.99,
    img: "./images/item-8.jpeg",
    desc: `on it tumblr kickstarter thundercats migas everyday carry squid palo santo leggings. Food truck truffaut  `,
  },
  {
    id: 9,
    title: "quarantine buddy",
    category: "3D-PRINT",
    price: 16.99,
    img: "../images/item-9.jpeg",
    desc: `skateboard fam synth authentic semiotics. Live-edge lyft af, edison bulb yuccie crucifix microdosing.`,
  },
  {
    id: 10,
    title: "Hand Bracelet",
    category: "ORNAMENTS",
    price: 22.99,
    img: "./assets/img/beads2.webp",
    desc: `skateboard fam synth authentic semiotics. Live-edge lyft af, edison bulb yuccie crucifix microdosing.`,
  },
];
// get parent element
const sectionCenter = document.querySelector(".section-center");
const btnContainer = document.querySelector(".btn-container");
// display all items when page loads
window.addEventListener("DOMContentLoaded", function () {
  diplayMenuItems(menu);
  displayMenuButtons();
});

function diplayMenuItems(menuItems) {
  let displayMenu = menuItems.map(function (item) {
    // console.log(item);
      
       return `<div class="col-sm-6 col-md-4 col-lg-3 m-2">
                <div class="card">
                    <img class="card-img-top" src="${item.img}" height="300px" alt="Card image cap">
                   
                    <div class="card-footer">
                        <span class="float-right fw-bold">${item.title}</span>
                      
                    </div>
                </div>
            </div>

                `;
   
  });
  displayMenu = displayMenu.join("");
  // console.log(displayMenu);

  sectionCenter.innerHTML = displayMenu;
}
function displayMenuButtons() {
  const categories = menu.reduce(
    function (values, item) {
      if (!values.includes(item.category)) {
        values.push(item.category);
      }
      return values;
    },
    ["all"]
  );
  const categoryBtns = categories
    .map(function (category) {
      return `<button type="button" class=" btn btn-outline-primary filter-btn" data-id=${category}>
          ${category}
        </button>`;
    })
    .join("");

  btnContainer.innerHTML = categoryBtns;
  const filterBtns = btnContainer.querySelectorAll(".filter-btn");
  console.log(filterBtns);

  filterBtns.forEach(function (btn) {
    btn.addEventListener("click", function (e) {
      // console.log(e.currentTarget.dataset);
      const category = e.currentTarget.dataset.id;
      const menuCategory = menu.filter(function (menuItem) {
        // console.log(menuItem.category);
        if (menuItem.category === category) {
          return menuItem;
        }
      });
      if (category === "all") {
        diplayMenuItems(menu);
      } else {
        diplayMenuItems(menuCategory);
      }
    });
  });
}
//Activemenu
let navItems = document.querySelectorAll(".nav-item");

navItems.forEach(navItem => {
  navItem.addEventListener("click", () => {
    document.querySelector(".active")?.classList.remove("active");
    navItem.classList.add("active");
    
    })
  
  });

