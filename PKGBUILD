# Maintainer: Tom's Tech Support
pkgname=niri-theme-manager
pkgver=0.1.0
pkgrel=1
pkgdesc='A small desktop theme switcher for the Niri compositor'
arch=('any')
url='https://github.com/Spruhantom/Tomos-niritheme-manager'
license=('MIT')
depends=('python' 'tk')
optdepends=(
  'niri: validate and apply compositor configuration'
  'xdg-utils: open the Niri configuration folder from the app'
)
makedepends=('git')
source=("${pkgname}::git+https://github.com/Spruhantom/Tomos-niritheme-manager.git#branch=main")
sha256sums=('SKIP')

package() {
  install -Dm755 "$srcdir/$pkgname/niri-theme-manager" \
    "$pkgdir/usr/bin/niri-theme-manager"
  install -Dm644 "$srcdir/$pkgname/niri_theme_manager.py" \
    "$pkgdir/usr/share/$pkgname/niri_theme_manager.py"
  install -Dm644 "$srcdir/$pkgname/niri-theme-manager.desktop" \
    "$pkgdir/usr/share/applications/niri-theme-manager.desktop"
  install -Dm644 "$srcdir/$pkgname/LICENSE" \
    "$pkgdir/usr/share/licenses/$pkgname/LICENSE"
  install -Dm644 "$srcdir/$pkgname/README.md" \
    "$pkgdir/usr/share/doc/$pkgname/README.md"
}
