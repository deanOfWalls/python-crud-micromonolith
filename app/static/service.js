function fetchPeople() {
  $.get("/person/", function (data) {
    const list = $("#personList");
    list.empty();
    data.forEach((p) => {
      list.append(`<li>${p.first_name} ${p.last_name} (Born: ${p.birth_date})</li>`);
    });
  });
}

$(document).ready(function () {
  fetchPeople();

  $("#personForm").submit(function (e) {
    e.preventDefault();
    const person = {
      first_name: $("#firstName").val(),
      last_name: $("#lastName").val(),
      birth_date: $("#birthDate").val(),
    };

    $.ajax({
      url: "/person/",
      method: "POST",
      contentType: "application/json",
      data: JSON.stringify(person),
      success: function () {
        fetchPeople();
        $("#personForm")[0].reset();
      },
      error: function () {
        alert("Failed to create person.");
      }
    });
  });
});
