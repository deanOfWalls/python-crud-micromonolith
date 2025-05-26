function fetchPeople() {
  $.get("/person/", function (data) {
    const list = $("#personList");
    list.empty();
    data.forEach((p) => {
      list.append(`<li>${p.id}: ${p.first_name} ${p.last_name} (Born: ${p.birth_date})</li>`);
    });
  });
}

function fetchById(id) {
  $.get(`/person/${id}`, function (person) {
    $("#firstName").val(person.first_name);
    $("#lastName").val(person.last_name);
    $("#birthDate").val(person.birth_date);
  }).fail(() => alert("Person not found."));
}

function updatePerson(id) {
  const person = {
    id,
    first_name: $("#firstName").val(),
    last_name: $("#lastName").val(),
    birth_date: $("#birthDate").val(),
  };

  $.ajax({
    url: `/person/${id}`,
    method: "PUT",
    contentType: "application/json",
    data: JSON.stringify(person),
    success: function () {
      fetchPeople();
      alert("Person updated.");
    },
    error: function () {
      alert("Update failed.");
    },
  });
}

function deletePerson(id) {
  $.ajax({
    url: `/person/${id}`,
    method: "DELETE",
    success: function () {
      fetchPeople();
      alert("Person deleted.");
    },
    error: function () {
      alert("Delete failed.");
    },
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
      },
    });
  });

  $("#fetchBtn").click(() => {
    const id = $("#personId").val();
    if (id) fetchById(id);
  });

  $("#updateBtn").click(() => {
    const id = $("#personId").val();
    if (id) updatePerson(id);
  });

  $("#deleteBtn").click(() => {
    const id = $("#personId").val();
    if (id) deletePerson(id);
  });
});
