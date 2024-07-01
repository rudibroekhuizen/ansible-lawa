# Ansible base role

## Variables

Enable or disable the UFW firewall by setting the firewall variable:

```
firewall: false # default is true
```

Set time related settings:

```
timezone: Europe/Amsterdam # Is the default. Check available entries with timedatectl list-timezones
ntp_servers:
  - 0.ubuntu.pool.ntp.org
  - 1.ubuntu.pool.ntp.org
maintenance_reboot_schedule: Mon 22:00:00 # Time in configured timezone
```

Set systemd-networkd-wait-online fix:

```yaml
systemd_networkd_wait_online_fix: true
```

To enable specific DNS servers. Disables any DNS servers obtained through DHCP.

```yaml
ubuntu_dns_servers:
  - 172.16.51.4
  - 172.16.51.5
```

This role implements a workaround for [this
issue](https://github.com/fwupd/fwupd/issues/3597) with the
`fwupd-refresh.service`. To disable this fix, set this variable:

```yaml
ubuntu_fwupd_refresh_fix: false
```

## N.B.

An enabled UFW firewall by default merely limits SSH sessions.
