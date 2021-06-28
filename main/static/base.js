var main = $('#products')
		var items = main.find(".items")
		items.each(function() {
			$(this).removeClass('d-none')
		})

		function search(e) {
			var text = new FormData();
			var text_ = e.target.value
			text.append('text', text_)
			var isID = true


			$.ajax({
				type: 'POST',
				url: '/forms/search',
				data: text,
				contentType: false,
				cache: false,
				processData: false,
				success: function(data) {
					items.each(function() {
						isID = false
						var item = $(this).attr("id")

						for (let i = 0; i < data['items'].length; i++) {
							if (item == data['items'][i]) {
								isID = true
								console.log('yup')
								break;
							}
							else {
								isID = false
							}
						}
						if (!isID) {
							$(this).addClass('d-none')
						} else {
							$(this).removeClass('d-none')
						}
					})
				}
		})
	}