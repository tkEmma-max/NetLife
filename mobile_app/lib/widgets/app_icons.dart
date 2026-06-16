import 'package:flutter/material.dart';
import 'package:flutter_svg/flutter_svg.dart';

class AppIcons {
  // Icônes SVG pour la navigation
  static Widget home({double size = 24, Color color = Colors.black}) {
    return SvgPicture.string(
      '''
      <svg width="$size" height="$size" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M3 12L12 3L21 12" stroke="$color" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        <path d="M5 10V20H19V10" stroke="$color" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        <path d="M9 20V14H15V20" stroke="$color" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
      ''',
      width: size,
      height: size,
    );
  }

  static Widget alerts({double size = 24, Color color = Colors.black}) {
    return SvgPicture.string(
      '''
      <svg width="$size" height="$size" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M12 2C12 2 3 7 3 16H21C21 7 12 2 12 2Z" stroke="$color" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        <path d="M12 22C13.6569 22 15 20.6569 15 19H9C9 20.6569 10.3431 22 12 22Z" stroke="$color" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
      ''',
      width: size,
      height: size,
    );
  }

  static Widget report({double size = 24, Color color = Colors.black}) {
    return SvgPicture.string(
      '''
      <svg width="$size" height="$size" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <circle cx="12" cy="12" r="10" stroke="$color" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        <path d="M12 8V12M12 16H12.01" stroke="$color" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
      ''',
      width: size,
      height: size,
    );
  }

  static Widget notifications({double size = 24, Color color = Colors.black}) {
    return SvgPicture.string(
      '''
      <svg width="$size" height="$size" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M18 8C18 6.4087 17.3679 4.88258 16.2426 3.75736C15.1174 2.63214 13.5913 2 12 2C10.4087 2 8.88258 2.63214 7.75736 3.75736C6.63214 4.88258 6 6.4087 6 8C6 15 3 17 3 17H21C21 17 18 15 18 8Z" stroke="$color" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        <path d="M13.73 21C13.5542 21.3031 13.3019 21.5547 12.9982 21.7295C12.6946 21.9044 12.3504 21.9965 12 21.9965C11.6496 21.9965 11.3054 21.9044 11.0018 21.7295C10.6982 21.5547 10.4458 21.3031 10.27 21" stroke="$color" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
      ''',
      width: size,
      height: size,
    );
  }

  static Widget profile({double size = 24, Color color = Colors.black}) {
    return SvgPicture.string(
      '''
      <svg width="$size" height="$size" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <circle cx="12" cy="8" r="4" stroke="$color" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        <path d="M20 21V19C20 16.7909 18.2091 15 16 15H8C5.79086 15 4 16.7909 4 19V21" stroke="$color" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
      ''',
      width: size,
      height: size,
    );
  }

  static Widget location({double size = 24, Color color = Colors.black}) {
    return SvgPicture.string(
      '''
      <svg width="$size" height="$size" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M12 21C12 21 20 15.5 20 10C20 5.58172 16.4183 2 12 2C7.58172 2 4 5.58172 4 10C4 15.5 12 21 12 21Z" stroke="$color" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        <circle cx="12" cy="10" r="3" stroke="$color" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
      ''',
      width: size,
      height: size,
    );
  }

  static Widget fire({double size = 24, Color color = Colors.black}) {
    return SvgPicture.string(
      '''
      <svg width="$size" height="$size" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M12 2C12 2 8 8 8 14C8 16.1217 8.84285 18.1566 10.3431 19.6569C11.8434 21.1571 13.8783 22 16 22C18.1217 22 20.1566 21.1571 21.6569 19.6569C23.1571 18.1566 24 16.1217 24 14C24 8 20 2 18 2C16 2 14 4 12 6C12 4 10 2 8 2C6 2 2 8 2 14C2 17.3137 3.525 20.5 6 22" stroke="$color" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
      ''',
      width: size,
      height: size,
    );
  }

  static Widget flood({double size = 24, Color color = Colors.black}) {
    return SvgPicture.string(
      '''
      <svg width="$size" height="$size" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M2 16L5 13L8 16L11 13L14 16L17 13L20 16L22 14" stroke="$color" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        <path d="M2 20L5 17L8 20L11 17L14 20L17 17L20 20L22 18" stroke="$color" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        <path d="M2 12L5 9L8 12L11 9L14 12L17 9L20 12L22 10" stroke="$color" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
      ''',
      width: size,
      height: size,
    );
  }

  static Widget waste({double size = 24, Color color = Colors.black}) {
    return SvgPicture.string(
      '''
      <svg width="$size" height="$size" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M3 6H21" stroke="$color" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        <path d="M8 6V4C8 3.46957 8.21071 2.96086 8.58579 2.58579C8.96086 2.21071 9.46957 2 10 2H14C14.5304 2 15.0391 2.21071 15.4142 2.58579C15.7893 2.96086 16 3.46957 16 4V6" stroke="$color" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        <path d="M19 6L18 20C18 20.5304 17.7893 21.0391 17.4142 21.4142C17.0391 21.7893 16.5304 22 16 22H8C7.46957 22 6.96086 21.7893 6.58579 21.4142C6.21071 21.0391 6 20.5304 6 20L5 6" stroke="$color" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
      ''',
      width: size,
      height: size,
    );
  }
}