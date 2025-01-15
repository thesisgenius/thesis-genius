-- Seed data for the `roles` table
INSERT INTO `roles` (`role_id`, `role_name`) VALUES
                                                 (1, 'Student'),
                                                 (2, 'Teacher'),
                                                 (3, 'Admin');

-- Seed data for the `users` table
INSERT INTO `users` (`user_id`, `first_name`, `last_name`, `email`, `username`, `password`, `role_id`, `is_admin`, `is_active`, `is_authenticated`, `created_at`, `updated_at`) VALUES
                                                                                                                                                                                    (1, 'Alice', 'Smith', 'alice@example.com', 'alice@example.com', 'hashed_password1', 1, 0, 1, 0, NOW(), NOW()),
                                                                                                                                                                                    (2, 'Bob', 'Johnson', 'bob@example.com', 'bob@example.com', 'hashed_password2', 2, 0, 1, 0, NOW(), NOW()),
                                                                                                                                                                                    (3, 'Charlie', 'Brown', 'charlie@example.com', 'charlie@example.com', 'hashed_password3', 3, 1, 1, 1, NOW(), NOW());

-- Seed data for the `theses` table
INSERT INTO `theses` (`thesis_id`, `title`, `abstract`, `status`, `student_id`, `created_at`, `updated_at`) VALUES
                                                                                                                (1, 'The Impact of AI on Education', 'This thesis explores how AI is transforming education.', 'Pending', 1, NOW(), NOW()),
                                                                                                                (2, 'Climate Change Mitigation Strategies', 'An analysis of effective climate change mitigation approaches.', 'Pending', 2, NOW(), NOW());

-- Seed data for the `posts` table
INSERT INTO `posts` (`id`, `user_id`, `title`, `description`, `content`, `created_at`, `updated_at`) VALUES
                                                                                                         (1, 1, 'Welcome to the Forum!', 'Feel free to discuss anything here.', 'This is the first post in the forum.', NOW(), NOW()),
                                                                                                         (2, 2, 'Thesis Tips', 'Here are some tips for writing a great thesis.', 'Content about thesis tips.', NOW(), NOW());

-- Seed data for the `post_comments` table
INSERT INTO `post_comments` (`id`, `user_id`, `post_id`, `content`, `created_at`, `updated_at`) VALUES
                                                                                                    (1, 1, 1, 'Thanks for starting this thread!', NOW(), NOW()),
                                                                                                    (2, 2, 2, 'Great tips, thank you!', NOW(), NOW());

-- Seed data for the `session_log` table
INSERT INTO `session_log` (`session_id`, `user_id`, `login_time`) VALUES
                                                                      (1, 1, NOW()),
                                                                      (2, 2, NOW());

-- Seed data for the `settings` table
INSERT INTO `settings` (`id`, `name`, `value`) VALUES
                                                   (1, 'site_name', 'ThesisGenius'),
                                                   (2, 'admin_email', 'admin@example.com');
