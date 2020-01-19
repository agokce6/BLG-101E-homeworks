from hash_passwd import create_hash

passwd = input("Please enter your password: ")

password_hash = create_hash(passwd)

comments = []

while True:
    comment = input("Enter your comment: ")
    user_passwd = input("Enter your password: ")
    user_passwd_hash = create_hash(user_passwd)
    if(password_hash == user_passwd_hash):
        comments.append(comment)
        print("Previously entered comments:")
        for i in range(len(comments)):
            print("%(index)d. %(comment)s" % {"index":i+1,"comment": comments[i]})
    else:
        print("I am sorry I can't let you do that")
