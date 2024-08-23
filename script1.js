// Xử lý sự kiện cho biểu mẫu nhập liệu
document.getElementById('submitForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const formData = new FormData(this);

    fetch('http://127.0.0.1:5000/submit', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        // Hiển thị thông báo
        const submitResult = document.getElementById('submitResult');
        submitResult.innerText = data.message || "Lỗi khi lưu dữ liệu";
        if (data.id) {
            submitResult.innerText += ` ID khách hàng: ${data.id}`;
        }
        
        // Đặt thời gian ẩn thông báo sau 20 giây
        setTimeout(() => {
            submitResult.innerText = "";  // Xóa thông báo sau 20 giây
        }, 20000); // 20000 ms = 20 giây
    })
    .catch(error => {
        console.error('Error in submit request:', error);
        document.getElementById('submitResult').innerText = "Có lỗi xảy ra!";
    });
});

// Xử lý sự kiện cho biểu mẫu tìm kiếm
document.getElementById('searchForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const searchName = document.getElementById('search_name').value;

    fetch(`http://127.0.0.1:5000/search?search_name=${encodeURIComponent(searchName)}`)
    .then(response => response.json())
    .then(data => {
        // Ghi log kết quả tìm kiếm
        console.log('Search result:', data);
        const searchResult = document.getElementById('searchResult');
        if (data.error) {
            searchResult.innerText = data.error;
        } else {
            searchResult.innerHTML = `<p>ID khách hàng: ${data.id}</p><p>Tên: ${data.name}</p><p>Cân nặng: ${data.weight}</p>`;
        }
    })
    .catch(error => {
        console.error('Error in search request:', error);
        document.getElementById('searchResult').innerText = "Có lỗi xảy ra!";
    });
});
