import numpy as np
import matplotlib.pyplot as plt


def draw_error_plot(errors: list) -> None:
    """Отрисовка графика изменения ошибки"""
    plt.plot(errors)
    plt.title("Error dynamic")
    plt.xlabel("iteration")
    plt.ylabel("error")
    plt.show()


class SVD_pp:
    def __init__(self, k: int, users: int, items: int, lr: float, l2_reg: float):
        """Инициализация параметров модели"""
        self.u = np.random.rand(users, k)
        self.v = np.random.rand(items, k)
        self.b_users = np.random.rand(users)
        self.b_items = np.random.rand(items)
        self.mu = np.random.random()
        self.lr = lr
        self.l2_reg = l2_reg

    def predict(self, user_id: int, item_id: int) -> float:
        """Предсказание оценки пользователя user_id для объекта item_id"""
        pred = self.mu + self.b_users[user_id] + self.b_items[item_id] + self.u[user_id].dot(self.v[item_id])
        return pred

    def update_user(self, index: int, data: np.array) -> None:
        """Обновляет модель для уже существующего пользователя"""
        self._update_model(index, data, obj_type="user")

    def update_item(self, index: int, data: np.array) -> None:
        """Обновляет модель для уже существующего объекта"""
        self._update_model(index, data, obj_type="item")

    def add_new_user(self, data: np.array) -> None:
        """Добававляет в модель нового пользователя и дообучает ее"""
        self.u = np.vstack((self.u, np.random.rand(1, self.u.shape[1])))
        self.b_users = np.hstack((self.b_users, np.random.random()))
        self._update_model(self.u.shape[0], data, obj_type="user")

    def add_new_item(self, data: np.array) -> None:
        """Добававляет в модель новый объект и дообучает ее"""
        self.v = np.vstack((self.v, np.random.rand(1, self.v.shape[1])))
        self.b_items = np.hstack((self.b_items, np.random.random()))
        self._update_model(self.v.shape[0], data, obj_type="item")

    def _update_model(self, i: int, data: np.array, obj_type="user") -> None:
        """обновление модели при добавлении нового объекта"""
        total_ratings = (~np.isnan(data)).sum()
        mse = 0
        errors = []
        old_mse = 0
        iter = 0
        while True:
            for j in np.where(~np.isnan(data))[0]:
                if obj_type == "user":
                    d = self.u[i].dot(self.v[j])
                else:
                    d = self.u[j].dot(self.v[i])

                err = data[j] - self.mu - self.b_users[i] - self.b_items[j] - d
                mse += err * err

                # обновим параметры
                self.mu += self.lr * err * self.mu

                if obj_type == "user":
                    self.b_users[i] += self.lr * (err - self.l2_reg * self.b_users[i])
                    self.u[i] += self.lr * (err * self.v[j] - self.l2_reg * self.u[i])
                else:
                    self.b_items[i] += self.lr * (err - self.l2_reg * self.b_items[i])
                    self.v[i] += self.lr * (err * self.u[j] - self.l2_reg * self.v[i])

            mse /= total_ratings
            # if iter % 10 == 0:
            #     print(f"Iteration #{iter}, MSE: {mse}")
            iter += 1
            errors.append(mse)

            if abs(mse - old_mse) < 0.0001:
                break

            old_mse = mse
            mse = 0

        # draw_error_plot(errors)

    def gradient_descent(self, interact_matrix: np.array) -> None:
        """Градиентный спуск"""
        mse = 0
        errors = []
        total_ratings = (~np.isnan(interact_matrix)).sum()
        old_mse = 0
        iter = 0
        while True:
            for i in range(interact_matrix.shape[0]):
                for j in np.where(~np.isnan(interact_matrix[i]))[0]:
                    err = interact_matrix[i][j] - self.mu - self.b_users[i] - self.b_items[j] - self.u[i].dot(self.v[j])
                    mse += err * err
                    # обновим параметры
                    self.mu += self.lr * err * self.mu
                    self.b_users[i] += self.lr * (err - self.l2_reg * self.b_users[i])
                    self.b_items[j] += self.lr * (err - self.l2_reg * self.b_items[j])
                    self.u[i] += self.lr * (err * self.v[j] - self.l2_reg * self.u[i])
                    self.v[j] += self.lr * (err * self.u[i] - self.l2_reg * self.v[j])

            mse /= total_ratings
            if iter % 10 == 0:
                print(f"Iteration #{iter}, MSE: {mse}")
            iter += 1
            errors.append(mse)

            if abs(mse - old_mse) < 0.0001:
                break

            old_mse = mse
            mse = 0

        # draw_error_plot(errors)
