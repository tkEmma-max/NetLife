class UserModel {
  final String id;
  final String username;
  final String email;
  final String? city;

  UserModel({
    required this.id,
    required this.username,
    required this.email,
    this.city,
  });

  factory UserModel.fromJson(Map<String, dynamic> json) {
    return UserModel(
      id: json['id'].toString(),
      username: json['username'] ?? 'Citoyen',
      email: json['email'] ?? '',
      city: json['city'] ?? 'Douala',
    );
  }
}