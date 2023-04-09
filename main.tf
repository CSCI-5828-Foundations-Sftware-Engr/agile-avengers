provider "google" {
  project = "seventh-port-360504"
  region = "us-west1-b"
}

resource "google_compute_firewall" "firewall" {
  name = "allow-5000"
  network = "default"
  allow {
    protocol = "tcp"
    ports = ["5000"]
  }
  source_ranges = ["0.0.0.0/0"]
  target_tags = ["allow-5000"]
}

resource "google_compute_instance" "vm_instance" {
  name = "vm-instance"
  machine_type = "f1-micro"
  zone = "us-west1-b"
  boot_disk {
    initialize_params {
      image = "ubuntu-os-cloud/ubuntu-2204-lts"
    }
  }

  metadata_startup_script = file("startup.sh")

  metadata = {
    ssh-keys = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQCye9Ze+SRZjDm9b7M3tJ1tdIJzpkhcfWRFjCUTbGzOKicmx4FMdcl8snqazWb9x+0UxQB3iK+gJzkKx6jnDmUmLp1KG0S+W8fU7U2FKzr8ubCvuLQYnKk0D1VSvAhg/c47Sp5sifzCHWt9ImFGxBQ7QeMB/c0nzH6gijdg+qBpxpCOFWOed0plNrJ5bwyoRxGVBg3bYtxu6JlsS6ghzWO3EoG6oxNQjTQGa6E9wMWfSJuYoVQoXrPqn2SaNG32gS80pW3SCV8hbMg+Bna6oqvsgPr1GsaFanAzKJ16Hof1RnfR1+ztILMFRq33rQfDX+AWnSbezl6BOar5/KnC/ZMEmH/5X4BQ/MwDeM2Pf7fJsNa3KsQi1LiEncg6dDk2aorZKaKP58UBmFiiZgOIkf/0V9P14EvuBVxMA3wEMZ2qN4QSj1W4R9U7n7wBLBwJN9p5n1ZEQOir6293BC0aoZ/f01CdWCC88IrrX+Ghy4aUb1xmTHg1jQQkyMXZOhkLSwc= aishwaryajayaram@cu-genvpn-tcom-10.180.148.100.int.colorado.edu"
    netrc = <<EOF
      machine github.com
      login AishwaryaJayaramu
      password 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
    EOF
  }

  tags = ["allow-5000"]
}
