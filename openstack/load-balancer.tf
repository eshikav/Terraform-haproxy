resource openstack_compute_instance_v2 "haproxy"{
    name            =   "haproxy-${count.index}"
    count           =   1
    flavor_name     =   ""
    image_id        =   ""
    security_groups =   [""]
    key_pair        =   ""
    network {
      name          =   ""
     }
    user_data       = "${file("${path.module}/user-data.txt")}"
}

resource openstack_compute_instance_v2 "webserver"{
    name            =   "webserver-${count.index}"
    count           =   2
    flavor_name     =   ""
    image_id        =   ""
    security_groups =   [""]
    key_pair        =   ""
    network {
      name          =   ""
     }
    user_data       = "${file("${path.module}/user-data.txt")}"
}

resource "openstack_compute_floatingip_associate_v2" "fip_1" {
  count             = 1
  floating_ip       = "${openstack_compute_floatingip_v2.haproxy.0.address}"
  instance_id       = "${openstack_compute_instance_v2.haproxy.0.id}"
  fixed_ip          = "${openstack_compute_instance_v2.haproxy.0.network.0.fixed_ip_v4}"
  depends_on        =  ["openstack_compute_instance_v2.haproxy","openstack_compute_floatingip_v2.haproxy"]
}

#Create Floating IP's
resource openstack_compute_floatingip_v2 "haproxy"{
   count            =  1
   pool             =  ""
}

resource "null_resource" "cluster" {
  triggers {
    cluster_instance_ids = "${join(",", openstack_compute_instance_v2.webserver.*.id)}"
     }
  provisioner "local-exec" {
    command        = "ansible-playbook configure-haproxy.yml -i dynamic-inventory.py --private-key=instance.pem -u centos"
                          }
  depends_on       = ["openstack_compute_instance_v2.haproxy","openstack_compute_floatingip_v2.haproxy","openstack_compute_floatingip_associate_v2.fip_1"]
  }
