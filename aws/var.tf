variable "instance"{
  description = " name of the instance"
  type = "string"
  default = "ami-bf4193c7"
}

variable "database"{
  description = "count of the number of instances"
  type = "string"
  default = 3
}

variable "webserver"{
  description = "count of the number of instances"
  type = "string"
  default = 2
}

