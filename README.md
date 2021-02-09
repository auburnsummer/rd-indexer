# RD Indexer

A script which indexes through sources and creates or updates an SQLite database.

It also rehosts the rdzips and images to a Backblaze bucket.

The sources are defined in a YAML file.

## How to use it

1. Create a file called `.env` in the same directory as the `.env.example` file.
2. Copy the contents of `.env.example` into `.env`.
3. Set up Backblaze hosting according to this guide: https://jross.me/free-personal-image-hosting-with-backblaze-b2-and-cloudflare-workers/
4. Fill out the `.env` file accordingly.
   * `HOSTED_FILES_PREFIX` is anything that goes before the filename in the URL of your files. For
     instance, if your file URLs look like `https://example.com/files/ehfaioehaowef.png` the
     `HOSTED_FILES_PREFIX` is `https://example.com/files/`

5. Install node.js and SQLite3 on your OS.
6. In this directory, run `npm install` to install the JavaScript dependencies.
7. If there isn't a directory called `db` in this directory, create it.
8. Start an SQLite3 shell in a new database in the `db` directory, eg:

       sqlite3 db/orchard.db

9. In the shell, execute the `sql/create.sql` script:

        .read sql/create.sql

   (or just copy paste the script in)

10. Exit the shell.

11. Run this command (replacing `<path to db>` with the path to the database file you made earlier):

        node lib/cli.js index <path to db> conf/sources.yml

12. It will run and make the database.

    * Right now sometimes it randomly freezes and I don't know why (Programming!). If this happens you can exit it with CTRL-C
      and start it again. It will resume from where it froze.

13. Upload it with

        node lib/cli.js upload <path to db>