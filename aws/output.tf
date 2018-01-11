output "public_ip"{
   sensitive = true
   value = ["${aws_instance.database.*.public_ip}"]
}

