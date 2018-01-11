provider "aws" {
   access_key = ""
   secret_key = ""
   region     = ""

}

#resource "aws_instance" "webserver" {
#  ami           = "${ var.instance }"
#  instance_type = "t2.micro"
#  count         = "${ var.webserver }"
#  key_name      = "${aws_key_pair.deployer.key_name}"
#  depends_on    = ["aws_key_pair.deployer"]
#}

resource "aws_instance" "database" {
  ami           = "${ var.instance }"
  instance_type = "t2.micro"
  count         = "${ var.database }"
  key_name      = "${aws_key_pair.deployer.key_name}"
#  user_data     = "${file("${path.module}/user-data.txt")}"
  depends_on    = ["aws_key_pair.deployer"]
}

resource "null_resource" "web" {
  depends_on    = ["aws_instance.database"]
  provisioner "local-exec" {
    command = "ansible-playbook /root/terraform_creation/galera-cluster.yml -i dynamic_inventory.py "
  }
}

resource "aws_key_pair" "deployer" {
    key_name = "deployer-key"
    public_key = "${file("${path.module}/id_rsa.pub")}"
}
