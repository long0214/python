var app = new Vue({
	el: '#app',
	name: 'app',
	data: {
		field_name: [], // 列名
		vpnlist_all: [], // get到的所有列表
		vpnlist_show: [], // 分页显示的列表
		vpnlist_select: [], // 选中的列表
		status_select: '',  // 状态选择
		search_text: '',   // 搜索内容
		page_row: 14   // 每页行数
	},
	methods: {
		// 状态选择
		select_changed: function (value, oldvalue) {
			var self = this;
			// 先设置vpnlist_show vpnlist_select为空
			self.vpnlist_show = []
			self.vpnlist_select = []
			// 查询
			axios({
				method: 'get',
				url: '/vpnmanage/get/' + value + '/',
				withCredentials: true
			})
				.then(function (resopnse) {
					self.field_name = resopnse.data.field_name
					self.vpnlist_all = resopnse.data.vpnlist
					self.vpnlist_show = self.vpnlist_all.slice(0, self.page_row)
					// console.log(self.vpnlist)
				})
				.catch(function (error) {
					console.log(error)
				})
		},
		// 分页
		page_changed: function (value) {
			var self = this;
			show_start = (value - 1) * self.page_row
			show_end = value * self.page_row
			self.vpnlist_show = self.vpnlist_all.slice(show_start, show_end)
		},
		// 搜索
		search: function () {
			var self = this;
			self.vpnlist_show = []
			// 遍历vpnlist_all
			// 如果search为空,返回
			if (self.search_text == '') {
                self.vpnlist_show = self.vpnlist_all
			}
			// 如果search非空,遍历vpnlist_all
			for (i=0;i<self.vpnlist_all.length;i++) {
				values = Object.values(self.vpnlist_all[i])
				if (values.indexOf(self.search_text) != -1) {
					self.vpnlist_show.push(self.vpnlist_all[i])
				}
			}
		},
		// checkbox选择
		checkbox_select: function (id) {
			var self = this;
			// 获取checkbox按钮,判断是否选中
			checkbox = document.getElementById(id).getElementsByTagName('input').checkbox
			if (checkbox.checked == true) {
				// 选中则添加
				self.vpnlist_all.forEach(function(item, index, array){
					if (item.id == id) {
						self.vpnlist_select.push(item)
					}
				});
			} else {
				// 未选中则删除
				self.vpnlist_select.forEach(function(item, index, array){
					if (item.id == id) {
						array.splice(index, 1)
					}
				})
			}
			// console.log(self.vpnlist_select)
		},
		// 申请VPN
		vpn_request: function () {
			var self = this;
            // 获取输入的数据
            for ( i in self.vpnlist_select) {
                id = self.vpnlist_select[i].id
                self.vpnlist_select[i].project_name = document.getElementById(id).getElementsByTagName('input').project_name.value
                self.vpnlist_select[i].user = document.getElementById(id).getElementsByTagName('input').user.value
                self.vpnlist_select[i].phone_number = document.getElementById(id).getElementsByTagName('input').phone_number.value
                self.vpnlist_select[i].bind_mac = document.getElementById(id).getElementsByTagName('input').bind_mac.value
            }
			// console.log(self.vpnlist_select)
			axios({
				method: 'post',
				url: '/vpnmanage/add/',
				data: self.vpnlist_select,
				withCredentials: true
			})
				.then(function (response) {
                    if (response.data.code!=0) {
                        alert(response.data.message)
                    } else {
                        // alert("申请完成!")
                        outlook = document.getElementById('add')
                        outlook.href = "mailto:zhaolei@cyou-inc.com?subject=" + "【VPN开通】"
                        outlook.href += "&body=各位好,%0A" + "%09请协助开通以下VPN:%0A"
                        outlook.href += "%09" + self.field_name.join("%09") + "%0A"
                        self.vpnlist_select.forEach(function (item, index, array){
                            outlook.href += "%09" + Object.values(item).join("%09") + "%0A"
                        })
                        outlook.click()
                        window.location.reload()
                        
                    }
				})
				.catch(function (error) {
					console.log(error)
				})
		},
        // 回收VPN
		vpn_delete: function () {
			var self = this;
			// console.log(self.vpnlist_select)
			axios({
				method: 'post',
				url: '/vpnmanage/delete/',
				data: self.vpnlist_select,
				withCredentials: true
			})
				.then(function (response) {
                    if (response.data.code == 0) {
                        alert("回收完成!")
                        outlook = document.getElementById('delete')
                        outlook.href = "mailto:zhaolei@cyou-inc.com?subject=" + "【VPN回收】"
                        outlook.href += "&body=各位好,%0A" + "%09请协助回收以下VPN:%0A"
                        outlook.href += "%09" + self.field_name.join("%09") + "%0A"
                        self.vpnlist_select.forEach(function (item, index, array){
                            outlook.href += "%09" + Object.values(item).join("%09") + "%0A"
                        })
                        outlook.click()
                        window.location.reload()
                    }
					console.log(response.data)
				})
				.catch(function (error) {
					console.log(error)
				})
		}
	},
	created: function () {
		var self = this;
		self.status_select = 'all';
	},	
	watch: {
		status_select: "select_changed",
	}

})
