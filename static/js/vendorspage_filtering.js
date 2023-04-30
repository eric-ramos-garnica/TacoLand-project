const filter_button = document.querySelector(".filter-image")
  filter_button.addEventListener('click',(e)=>{
    document.getElementById("container-filter-business-type").setAttribute('style','display:none;');
    document.getElementById("container-filters").removeAttribute('style');
  });
  
  const cancel_button_filter = document.getElementById('cancel-button-filter')
  cancel_button_filter.addEventListener('click',(e)=>{
      e.preventDefault();
      document.getElementById("container-filters").setAttribute('style','display:none;');
      document.getElementById("container-filter-business-type").removeAttribute('style');
  });