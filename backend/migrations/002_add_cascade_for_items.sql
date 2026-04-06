ALTER TABLE item_tag_mappings RENAME TO item_tag_mappings_old;

CREATE TABLE item_tag_mappings (
    item_id INTEGER,
    tag_id INTEGER,
    FOREIGN KEY(item_id) REFERENCES items(id) ON DELETE CASCADE,
    FOREIGN KEY(tag_id) REFERENCES tags(id) ON DELETE CASCADE,
    PRIMARY KEY(item_id, tag_id)
);

INSERT INTO item_tag_mappings SELECT * FROM item_tag_mappings_old;


ALTER TABLE item_attachment_mappings RENAME TO item_attachment_mappings_old;

CREATE TABLE item_attachment_mappings (
    id INTEGER PRIMARY KEY,
    item_id INTEGER,
    attachment_path TEXT,
    FOREIGN KEY(item_id) REFERENCES items(id) ON DELETE CASCADE
);

INSERT INTO item_attachment_mappings SELECT * FROM item_attachment_mappings_old;

DROP TABLE item_tag_mappings_old;
DROP TABLE item_attachment_mappings_old;