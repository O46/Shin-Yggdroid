"""
Creator: o46
Date: 02/27/2023
Updated: 03/03/2023
Summary: performs basic arithmatic on a given number with a length of 15 or higher to generate an RGB color code.
"""


def conv_num(num, r_one, r_two, round_val):
    """
    :param num:
    :param r_one:
    :param r_two:
    :param round_val:
    :return:
    """
    num = int(num[r_one:r_two])
    num = round(num / round_val)
    return num


def id_to_color(provided_id: str = "0", l_min_range: int = -5, l_max_range: int = None,
                m_min_range: int = -11, m_max_range: int = -6,
                r_min_range: int = -16, r_max_range: int = -11,
                round_val=391):
    """
    Converts a given ID with a length of 15 or more in to an RGB color value.
    :param provided_id:
    :param l_min_range:
    :param l_max_range:
    :param m_min_range:
    :param m_max_range:
    :param r_min_range:
    :param r_max_range:
    :param round_val:
    :return: bool, string, tuple or None
    """
    if len(str(provided_id)) < 15:
        return False, f"ID insufficiently long, length of {len(id)}.", 0
    elif round_val == 0:
        return False, "Divisor cannot be 0", 0
    else:
        print(f"User ID\n-------\n{provided_id[l_min_range:l_max_range]}\n{provided_id[m_min_range:m_max_range]}\n"
              f"{provided_id[r_min_range:r_max_range]}\n")
        first_num = conv_num(provided_id, l_min_range, l_max_range, round_val)
        second_num = conv_num(provided_id, m_min_range, m_max_range, round_val)
        third_num = conv_num(provided_id, r_min_range, r_max_range, round_val)
        print(f"Alt Nums\n-------\n{first_num}\n{second_num}\n{third_num}\n")
        return True, "Success", (first_num, second_num, third_num)


if __name__ == "__main__":
    user_id = input("Enter User ID: ")  # 87685931527606272
    color_output = id_to_color(user_id)
    """while True:
        try:
            user_id = int(input("Enter User ID: "))
            print(id_to_color(user_id))
        except ValueError as val_err:
            print(f"Error: {val_err}.\nPlease provide a valid integer.")"""
    print(f"https://convertingcolors.com/rgb-color-{color_output[2][0]}_{color_output[2][1]}_{color_output[2][2]}.html")
