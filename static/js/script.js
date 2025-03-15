$(document).ready(function () {
    function fetchData() {
        $.ajax({
            url: '/get-post-data',
            method: 'GET',
            success: function (data) {
                $('#dataTable').empty(); // Clear table before appending
                data.forEach((post, index) => {
                    console.log(post)
                    let row = `
    <tr>
        <th scope="row">${index + 1}</th>
        <td>${post.post_id}</td>
        <td>${post.base_url.length > 250 ? post.base_url.substring(0, 250) + '...' : post.base_url}</td>
        ${post.caption ? `<td>${post.caption.length > 250 ? post.caption.substring(0, 250) + '...' : post.caption}</td>` : '<td>No Comment Found</td>'}
        <td><button data-id="${post.post_id}" class="get_summary btn btn-primary">do twitte</button></td>
    </tr>
`;

                    $('#dataTable').append(row);
                });
            },
            error: function (err) {
                console.log('Error fetching data:', err);
            }
        });
    }

    // Fetch immediately on page load
    fetchData();

    // Fetch data every 5 minutes (5 * 60 * 1000 ms)
    setInterval(fetchData, 5 * 60 * 1000);
});
$('#fetchData').click(function () {

    $.ajax({
        url: '/start_fetch_post',
        method: 'GET',
        success: function (data) {

        },
        error: function (err) {
            console.log('Error fetching data:', err);
        }
    });
});

$(document).on('click', '.do_post', function () {
    const post_id = $(this).attr('data-id');
    let caption = $('#popupText').val()


    $.ajax({
        url: '/post-tweet',
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ caption: caption }),
        success: function (response) {
            alert(response.message);
        },
        error: function (err) {
            const errorMsg = err.responseJSON ? err.responseJSON.message : 'Something went wrong!';
            alert(errorMsg);
        }
    });
});
$('#dataTable').on('click', '.get_summary', function () {
    const post_id = $(this).attr('data-id');

    if (!post_id) {
        alert('Caption is required!');
        return;
    }

    $.ajax({
        url: '/get_caption',
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ post_id: post_id }),
        success: function (response) {
            $('#overlay').show();
            $('#popupContainer').show();
            $('#popupText').val(response); // Clear text area
            $(".do_post").attr("data-id", post_id);


        },
        error: function (err) {
            const errorMsg = err.responseJSON ? err.responseJSON.message : 'Something went wrong!';
            alert(errorMsg);
        }
    });
});


$('#closePopup').click(function () {
    $('#overlay').hide();
    $('#popupContainer').hide();
    $('#popupText').val(''); // Clear text area
});

