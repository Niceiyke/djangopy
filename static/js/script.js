
  const opi =document.querySelectorAll('.opi')
  console.log(opi)
  console.log(3)

  console.log('3')
  
  opi.forEach(i => {
    if ((i.textContent)> 70){
      i.classList.add('opi-green')
      console.log(i.textContent)
    }
    if((i.textContent) < 70){
      i.classList.add('opi-red')
      console.log(i.textContent)
    }
    
  });


var car = [6, 7, 8];
console.log(car);
const equipment = document.getElementById("id_equipment");
const bConveyor = document.getElementById("div_id_bottle_conveyor");
bConveyor.style.display = "none";



equipment.addEventListener("change", (i) => {
  if (i.target.value == 9) {
    bConveyor.style.display = "block";
  } else {
    bConveyor.style.display = "none";
  }
});

