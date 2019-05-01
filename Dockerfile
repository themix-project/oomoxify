FROM archlinux/base

WORKDIR /opt/oomoxify
ENTRYPOINT /bin/bash

# Test dependensies:
RUN echo "Update arch deps 2018-12-19" && \
    echo -e 'Server = http://archlinux.cu.be/$repo/os/$arch\nServer = http://mirror.metalgamer.eu/archlinux/$repo/os/$arch' > /etc/pacman.d/mirrorlist && \
    pacman -Syu --noconfirm && \
    pacman -S --needed --noconfirm bash findutils shellcheck && \
    rm -fr /var/cache/pacman/pkg/ /var/lib/pacman/sync/

COPY . /opt/oomoxify/
